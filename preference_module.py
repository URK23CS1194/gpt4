def analyze_preferences(profile):
    interests = [x.strip() for x in profile.get("interests", "").split(",") if x.strip()]
    return {
        "primary_interest": interests[0] if interests else profile.get("preferred_category", "General learning"),
        "secondary_interests": interests[1:],
        "skill_level": profile.get("skill_level", "Beginner"),
        "learning_goal": profile.get("goal", ""),
        "preferred_type": profile.get("preferences", "Not specified"),
        "important_constraints": [
            f"Difficulty should suit {profile.get('skill_level', 'Beginner')} level",
            f"Return no more than {profile.get('number_of_items', 5)} courses"
        ]
    }
