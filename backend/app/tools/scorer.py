from typing import Any, Dict, List

from app.recommender import recommend_songs


def clamp_k(k: int, minimum: int = 1, maximum: int = 10) -> int:
    return max(minimum, min(maximum, int(k)))


def score_recommendations(
    intent: Dict[str, Any], songs: List[Dict], k: int = 5
) -> List[Dict[str, Any]]:
    user_prefs = {
        "favorite_genre": intent.get("favorite_genre", ""),
        "favorite_mood": intent.get("favorite_mood", ""),
        "target_energy": float(intent.get("target_energy", 0.60)),
    }
    return recommend_songs(user_prefs, songs, k=clamp_k(k))

