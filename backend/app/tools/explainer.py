from typing import Any, Dict, List


def explain_recommendation(
    intent: Dict[str, Any], recommendation: Dict[str, Any]
) -> str:
    song = recommendation["song"]
    reasons: List[str] = recommendation.get("reasons", [])
    matched = []

    if any(reason.startswith("genre match") for reason in reasons):
        matched.append(f"the {intent.get('favorite_genre')} genre cue")
    if any(reason.startswith("mood match") for reason in reasons):
        matched.append(f"the {intent.get('favorite_mood')} mood cue")
    if any(reason.startswith("energy similarity") for reason in reasons):
        matched.append("your target energy")

    if matched:
        detail = ", ".join(matched)
        return (
            f"Recommended because {song['title']} by {song['artist']} lines up with "
            f"{detail}."
        )

    return (
        f"Recommended because {song['title']} by {song['artist']} is one of the "
        "closest available catalog matches."
    )


def explain_recommendations(
    intent: Dict[str, Any], recommendations: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    explained = []
    for rank, recommendation in enumerate(recommendations, start=1):
        song = recommendation["song"]
        explained.append(
            {
                "rank": rank,
                "song": song,
                "score": round(recommendation["score"], 2),
                "reasons": recommendation["reasons"],
                "explanation": explain_recommendation(intent, recommendation),
            }
        )
    return explained

