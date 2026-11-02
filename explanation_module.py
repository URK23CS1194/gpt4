def explain_recommendations(recommendations, profile):
    explanations = []
    interests = profile.get("interests", "")
    for rec in recommendations:
        explanations.append({
            "course_name": rec.get("course_name", ""),
            "explanation": f"This course is recommended because its description or skills relate to {interests or profile.get('preferred_category', 'your selected learning category')} and your {profile.get('skill_level', 'selected')} skill level."
        })
    return explanations
