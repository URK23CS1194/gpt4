from utils import search_dataset

def refine_recommendations(df, profile, current_recommendations, feedback, model="llama3.2"):
    updated = dict(profile)
    updated["interests"] = (profile.get("interests", "") + ", " + feedback).strip(", ")
    updated["preferences"] = (profile.get("preferences", "") + "; Feedback: " + feedback).strip("; ")
    current_names = {r.get("course_name") for r in current_recommendations}
    candidates = search_dataset(df, updated, limit=60)
    filtered = [c for c in candidates if c.get("course_name") not in current_names]
    return (filtered or candidates)[:profile.get("number_of_items", 5)]
