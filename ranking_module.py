def rank_recommendations(recommendations):
    return sorted(recommendations, key=lambda x: float(x.get("score", 0)), reverse=True)
