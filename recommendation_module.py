import json, re, requests
from utils import search_dataset

def _ollama_personalize(candidates, profile, analysis, model):
    prompt = f"""You are a course recommendation assistant. Select and rank the best courses from this dataset candidate list.
User profile: {json.dumps(profile)}
Preference analysis: {json.dumps(analysis)}
Candidates (JSON): {json.dumps(candidates, ensure_ascii=False)}
Return ONLY a JSON array. Each item must contain course_name, score (0-100), reason.
Use only exact course_name values from candidates. Return at most {profile['number_of_items']} items."""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=120
        )
        response.raise_for_status()
        raw = response.json().get("response", "")
        match = re.search(r"\[.*\]", raw, re.S)
        if not match:
            return None
        data = json.loads(match.group(0))
        return data if isinstance(data, list) else None
    except Exception:
        return None

def generate_recommendations(df, profile, analysis, model="llama3.2"):
    candidates = search_dataset(df, profile, limit=40)
    if not candidates:
        return [], "No matching courses were found in the dataset."
    ai = _ollama_personalize(candidates, profile, analysis, model)
    by_name = {c["course_name"]: c for c in candidates}
    results = []
    if ai:
        for item in ai:
            name = item.get("course_name")
            if name in by_name:
                rec = dict(by_name[name])
                rec["score"] = max(0, min(100, int(float(item.get("score", rec["score"])))))
                rec["reason"] = str(item.get("reason", rec["reason"]))
                rec["explanation"] = rec["reason"]
                results.append(rec)
    if not results:
        results = candidates[:profile["number_of_items"]]
        status = "Ollama was unavailable or returned an invalid response. Dataset-based matching is being used instead."
    else:
        status = "Recommendations personalized by Ollama using your profile and dataset."
    return results[:profile["number_of_items"]], status
