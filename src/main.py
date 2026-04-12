"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from pathlib import Path

try:
    from src.recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs

# Project root (parent of `src/`), so data path works whether you run from repo root or from `src/`
_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
_SONGS_CSV = _DATA_DIR / "songs.csv"


def main() -> None:
    songs = load_songs(str(_SONGS_CSV))
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile (keys must match score_song / README)
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        song = rec["song"]
        score = rec["score"]
        reasons = rec["reasons"]
        explanation = "; ".join(reasons)
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
