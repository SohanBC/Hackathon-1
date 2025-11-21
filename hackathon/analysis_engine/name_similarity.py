# analysis_engine/reports/name_similarity.py
import re
from difflib import SequenceMatcher

def normalize_text(s: str):
    return re.sub(r'[^a-z0-9]','', (s or "").lower())

def similarity_ratio(a: str, b: str):
    return SequenceMatcher(None, a, b).ratio() if a and b else 0.0

def check_package_label_similarity(play_data):
    pkg = play_data.get("appId") or play_data.get("appId") or ""
    title = play_data.get("title") or ""
    pkg_n = normalize_text(pkg)
    title_n = normalize_text(title)
    sim = similarity_ratio(pkg_n, title_n)
    # simplistic brand match using small brand list (extend in DB)
    KNOWN = ["phonepe","paytm","gpay","upi","sbi","icici","hdfc","paypal"]
    best_brand = None
    best_score = 0.0
    for b in KNOWN:
        s = similarity_ratio(title_n, normalize_text(b))
        if s > best_score:
            best_score, best_brand = s, b
    return {"available": True, "score": (sim*0.6 + best_score*0.4), "details": {"package": pkg, "title": title, "pkg_title_similarity": round(sim,3), "best_brand": best_brand, "best_brand_score": round(best_score,3)}}

def check_reviews_histogram(play):
    hist = play.get("histogram")
    if not hist:
        return {"available": False}
    total = sum(hist) or 1
    five_pct = hist[4]/total
    one_pct = hist[0]/total
    # simple score: high five_pct but reasonable total => ok
    score = max(0.0, min(1.0, 1.0 - abs(five_pct - 0.2)))
    return {"available": True, "score": score, "details": {"histogram": hist, "5_star_pct": round(five_pct,3), "1_star_pct": round(one_pct,3)}}

def check_installs_vs_reviews(play):
    installs_raw = play.get("installs") or ""
    import re, math
    m = re.search(r"([\d,]+)", installs_raw)
    if not m:
        return {"available": False}
    installs = int(m.group(1).replace(",",""))
    ratings = play.get("ratings") or 0
    # heuristic: if installs tiny and ratings huge -> suspicious
    if installs < 1000 and ratings > 10000:
        return {"available": True, "score": 0.0, "details": {"installs": installs, "ratings": ratings, "suspicious": True}}
    # otherwise compute a normalized safety score
    score = max(0.0, min(1.0, 1.0 - (math.log1p(ratings+1)/(math.log1p(installs+1)+1e-6))*0.5))
    return {"available": True, "score": score, "details": {"installs": installs, "ratings": ratings}}
    
def developer_presence(play):
    dev = play.get("developer")
    dev_email = play.get("developerEmail")
    return {"available": bool(dev), "score": 1.0 if dev else 0.0, "details": {"developer": dev, "email": dev_email}}
