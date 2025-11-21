# analysis_engine/engine.py

"""
Central analysis engine.
Handles:
1. Store-only scoring (metadata from Play Store only)
2. Deep APK scoring (manifest, certs, URLs, icon hash, etc.)
"""

import os
import io
import re
import json
import time
import hashlib
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, List

from PIL import Image
from imagehash import phash
from androguard.misc import AnalyzeAPK

# Store-only report builder
from .reports.json_report import build_store_report
from .reports.score_weights import WEIGHTS


# ============================================================
# 1. STORE-ONLY ANALYSIS (Play Store metadata only)
# ============================================================

def analyze_store_only(play_data):
    """
    Orchestrates store-only checks and returns:
    - per-signal results (pkg/title, reviews, installs, developer)
    - risk_score (0..100)
    """
    report = build_store_report(play_data, WEIGHTS)
    return report



# ============================================================
# 2. APK FULL DEEP ANALYSIS (icon, certs, manifest, URLs, etc.)
# ============================================================

def _safe_phash(img_bytes: bytes) -> str | None:
    try:
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        return str(phash(img))
    except Exception:
        return None


def _sha1_hex(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _extract_urls(resource_strings) -> list:
    try:
        blob = str(resource_strings)
        found = re.findall(r"https?://[^\s\"'<>()]+", blob)
        return list(dict.fromkeys(found))
    except:
        return []


def analyze_apk_full(apk_bytes: Optional[bytes] = None,
                     apk_path: Optional[str] = None,
                     keep_temp: bool = False) -> Dict[str, Any]:
    """
    Full APK analysis using Androguard:
    - identity info
    - manifest + components
    - certificates (sha1/sha256)
    - icon perceptual hash
    - extracted URLs
    - native libs, assets, dex stats
    """

    tmp_file = None

    # Must have bytes or valid path
    if apk_bytes is None and apk_path is None:
        return {"success": False, "error": "No APK source provided"}

    try:
        # Write bytes to temp
        if apk_bytes is not None:
            t = tempfile.NamedTemporaryFile(delete=False, suffix=".apk")
            t.write(apk_bytes)
            t.flush()
            t.close()
            tmp_file = t.name
            apk_to_open = tmp_file
        else:
            apk_to_open = apk_path

        # Sanity check
        if not apk_to_open or not os.path.exists(apk_to_open):
            return {"success": False, "error": f"APK not found: {apk_to_open}"}

        # Run Androguard
        try:
            a, d, dx = AnalyzeAPK(apk_to_open)
        except Exception as e:
            return {"success": False, "error": f"Androguard failed: {e}"}

        # ---------------------------
        # Identity
        # ---------------------------
        identity = {
            "package": a.get_package(),
            "versionName": a.get_androidversion_name(),
            "versionCode": a.get_androidversion_code(),
            "minSdk": a.get_min_sdk_version(),
            "targetSdk": a.get_target_sdk_version(),
        }

        # ---------------------------
        # Certificates
        # ---------------------------
        certificates = []
        try:
            certs = a.get_certificates() or []
            for c in certs:
                if isinstance(c, (bytes, bytearray)):
                    der = bytes(c)
                else:
                    der = getattr(c, "original", None) or str(c).encode()

                certificates.append({
                    "sha1": _sha1_hex(der),
                    "sha256": _sha256_hex(der),
                })
        except:
            certificates = []

        # ---------------------------
        # Manifest components
        # ---------------------------
        manifest = {
            "permissions": a.get_permissions() or [],
            "activities": a.get_activities() or [],
            "services": a.get_services() or [],
            "receivers": a.get_receivers() or [],
            "providers": a.get_providers() or [],
            "intent_filters": a.get_intent_filters() or {}
        }

        # ---------------------------
        # Icon pHash
        # ---------------------------
        icon_hash = None
        try:
            icon_dat = a.get_app_icon()
            if isinstance(icon_dat, (bytes, bytearray)):
                icon_hash = _safe_phash(icon_dat)
            elif isinstance(icon_dat, str) and os.path.exists(icon_dat):
                with open(icon_dat, "rb") as f:
                    icon_hash = _safe_phash(f.read())
        except:
            icon_hash = None

        # ---------------------------
        # Extract URLs from resources
        # ---------------------------
        urls_found = []
        try:
            res = a.get_android_resources()
            if res:
                strings = res.get_strings()
                urls_found = _extract_urls(strings)
        except:
            pass

        # ---------------------------
        # Files list metadata
        # ---------------------------
        files = []
        try:
            files = list(a.get_files() or [])
        except:
            files = []

        native_libs = [f for f in files if f.endswith(".so")]
        assets = [f for f in files if f.startswith("assets/")]

        # ---------------------------
        # Simple DEX stats
        # ---------------------------
        dex_stats = {
            "num_classes": None,
            "num_methods": None,
            "classes_sample": []
        }

        try:
            classes = dx.get_classes_names() or []
            dex_stats["num_classes"] = len(classes)
            dex_stats["classes_sample"] = classes[:20]

            methods = list(dx.get_methods())
            dex_stats["num_methods"] = len(methods)

        except:
            pass

        # ---------------------------
        # Heuristics (useful for scoring)
        # ---------------------------
        perms = manifest["permissions"]
        heuristics = {
            "has_overlay": any("SYSTEM_ALERT_WINDOW" in p for p in perms),
            "has_native_libs": len(native_libs) > 0,
            "asset_count": len(assets),
        }

        # ---------------------------
        # Build final response
        # ---------------------------
        report = {
            "identity": identity,
            "certificates": certificates,
            "manifest": manifest,
            "icon_hash": icon_hash,
            "urls_found": urls_found,
            "files": {
                "all": files,
                "native_libs": native_libs,
                "assets": assets
            },
            "dex": dex_stats,
            "heuristics": heuristics,
            "analysis_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

        return {"success": True, "apk": report}

    finally:
        # Cleanup temporary file
        if (apk_bytes is not None) and (tmp_file is not None) and (not keep_temp):
            try:
                os.remove(tmp_file)
            except:
                pass
