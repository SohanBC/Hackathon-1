# backend/routes/scan_apk.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from analysis_engine.engine import analyze_apk_full
from analysis_engine.engine import analyze_store_only
from backend.services.scoring_connector import call_scoring_engine

router = APIRouter()


@router.post("/scan/apk")
async def scan_apk(file: UploadFile = File(...)):
    """
    Deep APK scan:
    1) Extract APK metadata (certs, manifest, icon hash, URLs)
    2) Score using scoring engine
    """
    try:
        apk_bytes = await file.read()

        apk_report = analyze_apk_full(apk_bytes)
        final_score = call_scoring_engine(apk_report)

        return {
            "file": file.filename,
            "apk_metadata": apk_report,
            "score": final_score
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
