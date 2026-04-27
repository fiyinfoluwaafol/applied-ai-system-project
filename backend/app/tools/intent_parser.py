import re
from dataclasses import asdict, dataclass
from typing import Iterable, List, Optional, Tuple


DEFAULT_ENERGY = 0.60
ENERGY_BY_MOOD = {
    "happy": 0.80,
    "chill": 0.38,
    "intense": 0.90,
    "relaxed": 0.42,
    "moody": 0.65,
    "focused": 0.42,
    "nostalgic": 0.52,
    "melancholic": 0.36,
    "euphoric": 0.86,
    "peaceful": 0.22,
    "confident": 0.72,
    "soulful": 0.48,
    "romantic": 0.42,
}

GENRE_SYNONYMS = {
    "hip hop": "hip-hop",
    "rap": "hip-hop",
    "lo fi": "lofi",
    "lofi beats": "lofi",
    "study beats": "lofi",
    "rnb": "r&b",
    "r and b": "r&b",
}

MOOD_SYNONYMS = {
    "upbeat": "happy",
    "sunny": "happy",
    "feel good": "happy",
    "calm": "chill",
    "relax": "chill",
    "relaxed": "relaxed",
    "study": "chill",
    "sad": "melancholic",
    "party": "euphoric",
    "gym": "intense",
    "workout": "intense",
    "run": "intense",
}

ENERGY_CUES = {
    "gym": (0.90, 3),
    "workout": (0.85, 3),
    "run": (0.88, 3),
    "high energy": (0.90, 3),
    "intense": (0.90, 3),
    "party": (0.86, 2),
    "upbeat": (0.82, 2),
    "sunny": (0.80, 2),
    "calm": (0.32, 2),
    "relax": (0.35, 2),
    "chill": (0.38, 2),
    "study": (0.40, 2),
    "focus": (0.42, 2),
    "sleep": (0.20, 3),
    "peaceful": (0.22, 2),
    "sad": (0.36, 2),
}

ACOUSTIC_TERMS = ["acoustic", "unplugged", "folk", "coffee shop"]


@dataclass
class ParsedIntent:
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    matched_terms: List[str]
    warnings: List[str]


def normalize_text(text: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", " ", text.lower())
    return re.sub(r"\s+", " ", normalized).strip()


def contains_term(normalized_text: str, term: str) -> bool:
    normalized_term = normalize_text(term)
    return f" {normalized_term} " in f" {normalized_text} "


def find_catalog_value(
    normalized_prompt: str, values: Iterable[str]
) -> Tuple[Optional[str], Optional[str]]:
    for value in sorted(set(values), key=len, reverse=True):
        if contains_term(normalized_prompt, value):
            return value, value
    return None, None


def find_synonym(
    normalized_prompt: str, synonyms: dict
) -> Tuple[Optional[str], Optional[str]]:
    for term, value in sorted(synonyms.items(), key=lambda item: len(item[0]), reverse=True):
        if contains_term(normalized_prompt, term):
            return value, term
    return None, None


def find_energy(
    normalized_prompt: str, fallback_mood: str
) -> Tuple[float, List[str], List[str]]:
    matches = []
    matched_terms: List[str] = []
    warnings: List[str] = []

    for term, (energy, strength) in ENERGY_CUES.items():
        if contains_term(normalized_prompt, term):
            matches.append((strength, term, energy))
            matched_terms.append(term)

    if matches:
        matches.sort(key=lambda item: item[0], reverse=True)
        chosen_strength, chosen_term, chosen_energy = matches[0]
        buckets = {"low" if energy < 0.45 else "high" if energy > 0.70 else "medium" for _, _, energy in matches}
        if len(buckets) > 1:
            warnings.append(
                f"Conflicting energy cues found; using '{chosen_term}' as the strongest cue."
            )
        return chosen_energy, matched_terms, warnings

    if fallback_mood in ENERGY_BY_MOOD:
        return ENERGY_BY_MOOD[fallback_mood], [], warnings

    return DEFAULT_ENERGY, [], warnings


def parse_intent(prompt: str, genres: Iterable[str], moods: Iterable[str]) -> dict:
    normalized_prompt = normalize_text(prompt)
    matched_terms: List[str] = []
    warnings: List[str] = []

    genre, genre_term = find_catalog_value(normalized_prompt, genres)
    if not genre:
        genre, genre_term = find_synonym(normalized_prompt, GENRE_SYNONYMS)
    if genre_term:
        matched_terms.append(genre_term)

    mood, mood_term = find_catalog_value(normalized_prompt, moods)
    if not mood:
        mood, mood_term = find_synonym(normalized_prompt, MOOD_SYNONYMS)
    if mood_term:
        matched_terms.append(mood_term)

    target_energy, energy_terms, energy_warnings = find_energy(normalized_prompt, mood or "")
    matched_terms.extend(term for term in energy_terms if term not in matched_terms)
    warnings.extend(energy_warnings)

    likes_acoustic = any(contains_term(normalized_prompt, term) for term in ACOUSTIC_TERMS)
    if likes_acoustic:
        matched_terms.extend(
            term for term in ACOUSTIC_TERMS if contains_term(normalized_prompt, term)
        )

    if not genre:
        warnings.append("No supported genre was detected; scoring across the full catalog.")
    if not mood:
        warnings.append("No supported mood was detected; using energy and any genre cues available.")
    if not matched_terms:
        warnings.append("No catalog-backed prompt terms were detected; returning broad recommendations.")

    intent = ParsedIntent(
        favorite_genre=genre or "",
        favorite_mood=mood or "",
        target_energy=round(target_energy, 2),
        likes_acoustic=likes_acoustic,
        matched_terms=list(dict.fromkeys(matched_terms)),
        warnings=warnings,
    )
    return asdict(intent)
