# analysis_engine/reports/score_weights.py
# Single source of truth for heuristic weights used by the store-only engine
WEIGHTS = {
    'icon_similarity': 0.30,
    'name_package_similarity': 0.25,
    'cert_key_mismatch': 0.20,
    'publisher_history': 0.10,
    'review_patterns': 0.15
}
