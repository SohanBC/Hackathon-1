# backend/routes/evidence.py

from fastapi import APIRouter, HTTPException
from datetime import datetime
import json
from pathlib import Path

router = APIRouter()

EVIDENCE_DIR = Path("storage/evidence_kits")
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/evidence")
async def generate_evidence(report: dict):
    """
    Accepts the final risk-score JSON and creates an evidence kit file.
    """
    try:
        package = report.get("package", "unknown")
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"evidence_{package}_{timestamp}.json"

        file_path = EVIDENCE_DIR / filename
        file_path.write_text(json.dumps(report, indent=4))

        return {
            "status": "success",
            "file": filename,
            "path": str(file_path)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
