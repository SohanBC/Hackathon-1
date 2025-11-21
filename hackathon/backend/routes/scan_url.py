# backend/routes/scan_url.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.scoring_connector import call_scoring_engine
from backend.services.url_scraper import fetch_playstore_metadata

router = APIRouter()

class URLScanRequest(BaseModel):
    url: str

@router.post("/scan/url")
async def scan_url(req: URLScanRequest):
    """
    Trigger a store-only analysis for a Play Store URL or package id.
    Returns a quick store-only risk score and a pointer to a deeper scan if needed.
    """
    pkg = req.url
    play_data = fetch_playstore_metadata(pkg)
    if not play_data:
        raise HTTPException(status_code=404, detail="Play Store metadata not available")
    score = call_scoring_engine(play_data)
    return {"package": play_data.get("appId", pkg), "score": score}
