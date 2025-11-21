# scripts/generate_viz.py
import os, json
from pathlib import Path
import matplotlib.pyplot as plt

viz_dir = Path("visuals")
viz_dir.mkdir(parents=True, exist_ok=True)

# signal importance (weights)
weights = {"icon_similarity":0.30,"name_package_similarity":0.20,"cert_key_mismatch":0.20,"publisher_history":0.10,"review_patterns":0.20}
labels = list(weights.keys())
sizes = [weights[k] for k in labels]

plt.figure(figsize=(6,6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.title("Signal importance (normalized)")
plt.savefig(viz_dir / "signal_importance_pie.png", bbox_inches='tight')
plt.close()

# coverage counts by source
coverage_counts = {"play_store":4,"apk":5,"telemetry":1}
plt.figure(figsize=(6,4))
plt.bar(list(coverage_counts.keys()), list(coverage_counts.values()))
plt.title("Signals available per data source")
plt.ylabel("Signals count")
plt.savefig(viz_dir / "coverage_bar.png", bbox_inches='tight')
plt.close()

# pipeline component counts
pipeline = {"ingest":3,"analysis":6,"scoring":3,"reporting":3}
plt.figure(figsize=(6,4))
plt.bar(list(pipeline.keys()), list(pipeline.values()))
plt.title("Pipeline stages — component counts")
plt.ylabel("Components")
plt.savefig(viz_dir / "pipeline_components.png", bbox_inches='tight')
plt.close()

summary = {"weights":weights, "coverage":coverage_counts, "pipeline":pipeline}
with open(viz_dir / "summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Visuals saved to", str(viz_dir.resolve()))
