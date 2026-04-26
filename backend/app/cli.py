"""
Command line runner for the Music Recommender Simulation.

Runs the recommender against multiple user profiles (standard and
adversarial) to stress-test scoring logic and surface biases.
"""

from pathlib import Path

try:
    from app.recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs

_DATA_DIR = Path(__file__).resolve().parent / "data"
_SONGS_CSV = _DATA_DIR / "songs.csv"

# ── Standard profiles ────────────────────────────────────────────────
# Each targets a clearly different listener archetype in the catalog.

STANDARD_PROFILES = [
    {
        "name": "High-Energy Pop",
        "prefs": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.85,
        },
    },
    {
        "name": "Chill Lofi",
        "prefs": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.38,
        },
    },
    {
        "name": "Deep Intense Rock",
        "prefs": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.90,
        },
    },
]

# ── Adversarial / edge-case profiles ────────────────────────────────
# Designed to expose weaknesses: conflicting preferences, over-weighting
# of genre, and unusual combos that don't match any song cleanly.

ADVERSARIAL_PROFILES = [
    {
        # Tests: genre says "classical" (peaceful, low energy) but energy
        # target is very high — the two signals conflict.  Reveals whether
        # genre dominates even when the energy fit is terrible.
        "name": "EDGE: Classical + High Energy (conflict)",
        "prefs": {
            "favorite_genre": "classical",
            "favorite_mood": "intense",
            "target_energy": 0.95,
        },
    },
    {
        # Tests: genre/mood combo that does NOT exist in the catalog.
        # No song is hip-hop + melancholic, so the system must fall back
        # to partial matches.  Exposes over-reliance on genre weight.
        "name": "EDGE: Hip-Hop Melancholic (no exact match)",
        "prefs": {
            "favorite_genre": "hip-hop",
            "favorite_mood": "melancholic",
            "target_energy": 0.50,
        },
    },
]


def print_profile_results(label: str, prefs: dict, songs: list) -> None:
    """Print top-5 recommendations for a single profile in a readable block."""
    recs = recommend_songs(prefs, songs, k=5)

    print("=" * 60)
    print(f"  PROFILE: {label}")
    print(
        f"  Genre: {prefs['favorite_genre']}  |  "
        f"Mood: {prefs['favorite_mood']}  |  "
        f"Energy: {prefs['target_energy']}"
    )
    print("=" * 60)

    for rank, rec in enumerate(recs, start=1):
        song = rec["song"]
        score = rec["score"]
        reasons = rec["reasons"]
        print(f"  #{rank}  {song['title']} by {song['artist']}")
        print(f"       Score: {score:.2f}  |  Reasons: {', '.join(reasons)}")
    print()


def main() -> None:
    songs = load_songs(str(_SONGS_CSV))

    print("\n>>> STANDARD PROFILES <<<\n")
    for profile in STANDARD_PROFILES:
        print_profile_results(profile["name"], profile["prefs"], songs)

    print("\n>>> ADVERSARIAL / EDGE-CASE PROFILES <<<\n")
    for profile in ADVERSARIAL_PROFILES:
        print_profile_results(profile["name"], profile["prefs"], songs)


if __name__ == "__main__":
    main()
