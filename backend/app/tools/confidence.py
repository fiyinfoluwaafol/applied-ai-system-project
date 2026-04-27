from typing import Any, Dict, List


MAX_SCORE = 4.0


def evaluate_confidence(
    intent: Dict[str, Any], recommendations: List[Dict[str, Any]]
) -> Dict[str, Any]:
    reasons: List[str] = []
    matched_terms = intent.get("matched_terms", [])

    if not recommendations:
        return {"label": "low", "score": 0.0, "reasons": ["no recommendations"]}

    top_score = float(recommendations[0]["score"])
    second_score = float(recommendations[1]["score"]) if len(recommendations) > 1 else 0.0
    score_strength = min(1.0, top_score / MAX_SCORE)
    score_gap = max(0.0, min(1.0, (top_score - second_score) / 2.0))
    specificity = min(1.0, len(matched_terms) / 3.0)

    confidence_score = (score_strength * 0.55) + (score_gap * 0.20) + (specificity * 0.25)

    if intent.get("favorite_genre"):
        reasons.append("matched genre")
    if intent.get("favorite_mood"):
        reasons.append("matched mood")
    if top_score >= 3.0:
        reasons.append("strong top recommendation")
    elif top_score >= 2.0:
        reasons.append("moderate top recommendation")
    else:
        reasons.append("weak top recommendation")
    if score_gap < 0.15:
        reasons.append("top results are close together")
    if not matched_terms:
        reasons.append("prompt was vague")

    if confidence_score >= 0.75:
        label = "high"
    elif confidence_score >= 0.45:
        label = "medium"
    else:
        label = "low"

    return {
        "label": label,
        "score": round(confidence_score, 2),
        "reasons": reasons,
    }

