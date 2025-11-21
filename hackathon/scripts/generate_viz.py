# scripts/generate_histogram.py

import matplotlib.pyplot as plt
import json
from pathlib import Path


def generate_histogram(api_response: dict, output_path="histogram.png"):
    """
    Generates a histogram image from any API response
    that contains score → signals → reviews → details → histogram[]
    """

    try:
        histogram = (
            api_response
            .get("score", {})
            .get("signals", {})
            .get("reviews", {})
            .get("details", {})
            .get("histogram", None)
        )

        if not histogram or not isinstance(histogram, list):
            raise ValueError("Histogram data not found in API response")

        # Draw histogram
        plt.figure(figsize=(6, 4))
        plt.bar([1, 2, 3, 4, 5], histogram)
        plt.title("App Store Review Histogram")
        plt.xlabel("Rating (1★ to 5★)")
        plt.ylabel("Count")
        plt.tight_layout()

        # Write file
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, bbox_inches="tight")
        plt.close()

        return {
            "success": True,
            "message": "Histogram generated successfully.",
            "file": str(output_path)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# -------------------------
# Example (Standalone Test)
# -------------------------
if __name__ == "__main__":
    sample_json = {
        "package": "com.instagram.android",
        "score": {
            "signals": {
                "reviews": {
                    "details": {
                        "histogram": [
                            16780286,
                            5587260,
                            7733214,
                            14254258,
                            121065774
                        ]
                    }
                }
            }
        }
    }

    print(generate_histogram(sample_json, "output/instagram_hist.png"))
