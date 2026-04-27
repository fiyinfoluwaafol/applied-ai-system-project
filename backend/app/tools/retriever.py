from pathlib import Path
from typing import Dict, List

from app.recommender import load_songs


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "songs.csv"


def retrieve_songs(csv_path: Path = DATA_PATH) -> List[Dict]:
    return load_songs(str(csv_path))


def catalog_genres(songs: List[Dict]) -> List[str]:
    return sorted({song["genre"] for song in songs})


def catalog_moods(songs: List[Dict]) -> List[str]:
    return sorted({song["mood"] for song in songs})

