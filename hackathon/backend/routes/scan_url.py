# backend/routes/scan_url.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.url_scraper import fetch_playstore_metadata
from backend.services.scoring_connector import call_scoring_engine

router = APIRouter()


class URLScanRequest(BaseModel):
    url: str


@router.post("/scan/url")
async def scan_url(req: URLScanRequest):
    """
    Store-only scan:
    - Extract package
    - Fetch Play Store metadata
    - Run scoring engine
    """
    pkg = req.url

    play_data = fetch_playstore_metadata(pkg)
    if not play_data:
        raise HTTPException(404, "Play Store metadata not found")

    score = call_scoring_engine(play_data)

    return {
        "package": play_data.get("appId", pkg),
        "score": score
    }
