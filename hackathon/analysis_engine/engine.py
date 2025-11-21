# analysis_engine/engine.py
from .reports.json_report import build_store_report
from .reports.score_weights import WEIGHTS

def analyze_store_only(play_data):
    """
    Orchestrates store-only checks and returns a report that includes:
    - per-signal results (pkg/title, reviews, installs, developer, icons)
    - risk_score (0..100) where low = risky
    """
    report = build_store_report(play_data, WEIGHTS)
    return report
