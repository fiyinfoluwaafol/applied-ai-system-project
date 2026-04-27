import csv
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass

# ── Evaluation experiment (Phase 4, Option A — Weight Shift) ─────────
# Original weights: GENRE 2.0, MOOD 1.0, ENERGY 1.0
# Experiment: halve genre (2.0 → 1.0), double energy (1.0 → 2.0) to test
# whether genre was over-weighted in the baseline scoring.
GENRE_MATCH_POINTS = 2.0
MOOD_MATCH_POINTS = 1.0
ENERGY_SIMILARITY_WEIGHT = 1.0

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = user_profile_to_dict(user)
        ranked = sorted(
            self.songs,
            key=lambda song: score_song(user_prefs, song_to_dict(song))[0],
            reverse=True,
        )
        if k <= 0:
            return []
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = score_song(user_profile_to_dict(user), song_to_dict(song))
        if reasons:
            return (
                f"{song.title} by {song.artist} is recommended because "
                f"{', '.join(reasons)}."
            )
        return f"{song.title} by {song.artist} is one of the closest available matches."

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file; returns a list of dicts with typed numeric fields."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if not row.get("id") or not str(row["id"]).strip():
                continue
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = int(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences (genre, mood, energy); returns (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    if song["genre"] == user_prefs["favorite_genre"]:
        score += GENRE_MATCH_POINTS
        reasons.append(f"genre match (+{GENRE_MATCH_POINTS:.1f})")

    if song["mood"] == user_prefs["favorite_mood"]:
        score += MOOD_MATCH_POINTS
        reasons.append(f"mood match (+{MOOD_MATCH_POINTS:.1f})")

    energy_diff = abs(song["energy"] - user_prefs["target_energy"])
    energy_score = max(0.0, ENERGY_SIMILARITY_WEIGHT - energy_diff)
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score:.2f})")

    return (score, reasons)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Dict[str, Any]]:
    """Score every song, rank by match score descending, and return the top k with scores and reasons."""
    scored: List[Dict[str, Any]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append({"song": song, "score": score, "reasons": reasons})

    ranked = sorted(scored, key=lambda row: row["score"], reverse=True)
    if k <= 0:
        return []
    return ranked[:k]


def song_to_dict(song: Song) -> Dict[str, Any]:
    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "genre": song.genre,
        "mood": song.mood,
        "energy": song.energy,
        "tempo_bpm": song.tempo_bpm,
        "valence": song.valence,
        "danceability": song.danceability,
        "acousticness": song.acousticness,
    }


def user_profile_to_dict(user: UserProfile) -> Dict[str, Any]:
    return {
        "favorite_genre": user.favorite_genre,
        "favorite_mood": user.favorite_mood,
        "target_energy": user.target_energy,
    }
