import os
from datetime import datetime

def save_recommendations(profile, recommendations):
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", "recommendations.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("PERSONALIZED RECOMMENDATION SYSTEM\n")
        f.write("=" * 45 + "\n")
        f.write(f"Generated: {datetime.now():%Y-%m-%d %H:%M}\n")
        f.write(f"User: {profile.get('name')}\n")
        f.write(f"Goal: {profile.get('goal')}\n\n")
        for i, r in enumerate(recommendations, 1):
            f.write(f"{i}. {r.get('course_name')}\n")
            f.write(f"University: {r.get('university')}\n")
            f.write(f"Difficulty: {r.get('difficulty')}\n")
            f.write(f"Rating: {r.get('rating')}\n")
            f.write(f"Suitability: {r.get('score')}%\n")
            f.write(f"Reason: {r.get('reason')}\n")
            f.write(f"URL: {r.get('url')}\n\n")
    return path
