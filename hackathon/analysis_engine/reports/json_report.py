# analysis_engine/reports/json_report.py
from .name_similarity import check_package_label_similarity
from .name_similarity import normalize_text
from .name_similarity import check_brand_match
from .certificate_check import ( )  # placeholder: certificate check needs APK
from datetime import datetime

def build_store_report(play_data, weights):
    # run available store-only checks
    pkg_label = check_package_label_similarity(play_data)
    # review/checks - placeholder functions included below or imported
    from .name_similarity import check_reviews_histogram, check_installs_vs_reviews, developer_presence
    reviews = check_reviews_histogram(play_data)
    installs = check_installs_vs_reviews(play_data)
    dev = developer_presence(play_data)

    # combine weights (simple weighted average)
    signals = {
        "package_label": pkg_label.get("score", 0.5) if pkg_label.get("available") else 0.5,
        "reviews": reviews.get("score", 0.5) if reviews.get("available") else 0.5,
        "installs_vs_reviews": installs.get("score", 0.5) if installs.get("available") else 0.5,
        "developer": dev.get("score", 0.5) if dev.get("available") else 0.5,
    }

    total_w = sum([weights.get('name_package_similarity',0.2),
                   weights.get('review_patterns',0.1),
                   weights.get('publisher_history',0.1)])
    # map weights to our signals (example mapping)
    weighted = {}
    weighted['aggregate'] = (
        signals['package_label'] * weights.get('name_package_similarity', 0.2) +
        signals['reviews'] * weights.get('review_patterns', 0.1) +
        signals['developer'] * weights.get('publisher_history', 0.1) +
        signals['installs_vs_reviews'] * 0.1
    ) / (weights.get('name_package_similarity',0.2)+weights.get('review_patterns',0.1)+weights.get('publisher_history',0.1)+0.1)

    risk_score = int(round(weighted['aggregate'] * 100))
    report = {
        "generated_at": datetime.utcnow().isoformat()+"Z",
        "signals": {
            "package_label": pkg_label,
            "reviews": reviews,
            "installs_vs_reviews": installs,
            "developer": dev
        },
        "risk_score": risk_score
    }
    return report
