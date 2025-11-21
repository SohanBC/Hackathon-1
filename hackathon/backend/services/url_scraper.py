# backend/services/url_scraper.py
"""
Light wrapper for Play Store metadata fetch.
In production use google-play-scraper (node) or google_play_scraper (python) with retries, caching and regional fallback.
"""
from google_play_scraper.features.app_details import app_details

def fetch_playstore_metadata(package_or_url: str):
    # Attempt to extract package id
    import re
    m = re.search(r"id=([A-Za-z0-9_.]+)", package_or_url)
    pkg = m.group(1) if m else package_or_url
    try:
        data = app_details(pkg, lang="en", country="in")
        return data
    except Exception:
        return None
