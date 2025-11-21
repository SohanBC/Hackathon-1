# backend/services/scoring_connector.py
from analysis_engine.engine import analyze_store_only

def call_scoring_engine(play_data):
    """
    Thin adaptor: call analysis engine and return a risk score dict.
    """
    report = analyze_store_only(play_data)
    # report should contain 'risk_score' (0..100)
    return report
