import os, re
import pandas as pd

DATASET_PATH = os.path.join("dataset", "Coursera.csv")

def load_dataset():
    if not os.path.exists(DATASET_PATH):
        return None
    try:
        df = pd.read_csv(DATASET_PATH)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception:
        return None

def _find_col(df, names):
    lookup = {c.lower().replace("_", " ").strip(): c for c in df.columns}
    for name in names:
        key = name.lower().replace("_", " ").strip()
        if key in lookup:
            return lookup[key]
    for c in df.columns:
        if any(n.lower() in c.lower() for n in names):
            return c
    return None

def search_dataset(df, profile, limit=40):
    name_col = _find_col(df, ["Course Name", "course"])
    uni_col = _find_col(df, ["University", "institution"])
    diff_col = _find_col(df, ["Difficulty Level", "difficulty"])
    rating_col = _find_col(df, ["Course Rating", "rating"])
    url_col = _find_col(df, ["Course URL", "url"])
    desc_col = _find_col(df, ["Course Description", "description"])
    skills_col = _find_col(df, ["Skills", "skill"])
    if not name_col:
        return []
    interests = [x.strip().lower() for x in profile.get("interests", "").split(",") if x.strip()]
    interests += [profile.get("preferred_category", "").lower(), profile.get("goal", "").lower()]
    interests = [x for x in interests if x and x != "other"]
    level = profile.get("skill_level", "Beginner").lower()
    rows = []
    for _, row in df.iterrows():
        course = str(row.get(name_col, ""))
        desc = str(row.get(desc_col, "")) if desc_col else ""
        skills = str(row.get(skills_col, "")) if skills_col else ""
        text = f"{course} {desc} {skills}".lower()
        score = 25
        matched = []
        for term in interests:
            words = [w for w in re.findall(r"[a-zA-Z0-9+#]+", term) if len(w) > 2]
            if words and any(w in text for w in words):
                score += 12
                matched.append(term)
        difficulty = str(row.get(diff_col, "Not specified")) if diff_col else "Not specified"
        if level in difficulty.lower():
            score += 15
        elif level == "beginner" and "beginner" in difficulty.lower():
            score += 10
        rating = row.get(rating_col, "") if rating_col else ""
        try:
            score += min(10, max(0, int(float(rating) * 2)))
        except Exception:
            pass
        score = min(99, score)
        rows.append({
            "course_name": course,
            "university": str(row.get(uni_col, "Not specified")) if uni_col else "Not specified",
            "difficulty": difficulty,
            "rating": str(rating) if rating_col else "N/A",
            "url": str(row.get(url_col, "")) if url_col else "",
            "description": desc[:500],
            "skills": skills[:300],
            "score": score,
            "reason": ("Matches: " + ", ".join(matched)) if matched else "Selected based on course information, difficulty and rating.",
            "explanation": ""
        })
    rows.sort(key=lambda x: x["score"], reverse=True)
    return rows[:limit]
