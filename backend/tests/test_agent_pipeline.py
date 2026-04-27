from fastapi.testclient import TestClient

from app.agent import MusicCuratorAgent
from app.main import app
from app.tools.confidence import evaluate_confidence
from app.tools.explainer import explain_recommendation
from app.tools.guardrails import evaluate_guardrails, validate_prompt
from app.tools.intent_parser import parse_intent
from app.tools.retriever import catalog_genres, catalog_moods, retrieve_songs
from app.tools.scorer import score_recommendations


def test_intent_parser_maps_common_prompt():
    songs = retrieve_songs()
    intent = parse_intent(
        "happy pop workout songs",
        catalog_genres(songs),
        catalog_moods(songs),
    )

    assert intent["favorite_genre"] == "pop"
    assert intent["favorite_mood"] == "happy"
    assert intent["target_energy"] == 0.85
    assert intent["likes_acoustic"] is False
    assert "pop" in intent["matched_terms"]
    assert "happy" in intent["matched_terms"]
    assert "workout" in intent["matched_terms"]


def test_intent_parser_supports_synonyms():
    songs = retrieve_songs()
    intent = parse_intent(
        "lo-fi study beats to relax",
        catalog_genres(songs),
        catalog_moods(songs),
    )

    assert intent["favorite_genre"] == "lofi"
    assert intent["favorite_mood"] == "chill"
    assert intent["target_energy"] <= 0.40


def test_retriever_loads_catalog():
    songs = retrieve_songs()

    assert len(songs) >= 19
    assert any(song["title"] == "Sunrise City" for song in songs)
    assert {"id", "title", "artist", "genre", "mood", "energy"}.issubset(songs[0])


def test_scorer_preserves_known_top_recommendation():
    songs = retrieve_songs()
    intent = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
    }

    results = score_recommendations(intent, songs, k=5)

    assert results[0]["song"]["title"] == "Sunrise City"
    assert results[0]["score"] > 3.0


def test_explainer_returns_song_specific_text():
    songs = retrieve_songs()
    intent = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
    }
    recommendation = score_recommendations(intent, songs, k=1)[0]

    explanation = explain_recommendation(intent, recommendation)

    assert "Sunrise City" in explanation
    assert "pop" in explanation


def test_confidence_labels_strong_match_higher_than_vague_prompt():
    songs = retrieve_songs()
    strong_intent = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "matched_terms": ["pop", "happy", "workout"],
    }
    vague_intent = {
        "favorite_genre": "",
        "favorite_mood": "",
        "target_energy": 0.60,
        "matched_terms": [],
    }

    strong = evaluate_confidence(
        strong_intent, score_recommendations(strong_intent, songs, k=5)
    )
    vague = evaluate_confidence(
        vague_intent, score_recommendations(vague_intent, songs, k=5)
    )

    assert strong["label"] == "high"
    assert strong["score"] > vague["score"]
    assert vague["label"] == "low"


def test_guardrails_reject_empty_and_warn_on_vague_prompt():
    try:
        validate_prompt("   ")
    except ValueError as error:
        assert "non-empty" in str(error)
    else:
        raise AssertionError("Expected empty prompt validation to fail")

    guardrails = evaluate_guardrails(
        "playlist please",
        {"matched_terms": [], "warnings": ["No catalog-backed prompt terms were detected."]},
        {"label": "low", "score": 0.2, "reasons": []},
        [{"song": {"title": "Example"}}],
    )

    assert guardrails["safe"] is True
    assert guardrails["requires_human_review"] is True
    assert guardrails["warnings"]


def test_music_curator_agent_returns_complete_response():
    response = MusicCuratorAgent().run("happy pop workout songs")

    assert response["recommendations"]
    assert response["recommendations"][0]["song"]["title"] == "Sunrise City"
    assert response["confidence"]["label"] == "high"
    assert response["guardrails"]["safe"] is True
    assert [step["step"] for step in response["trace"]] == [
        "intent_parser",
        "retriever",
        "scorer",
        "explainer",
        "confidence",
        "guardrails",
    ]


def test_fastapi_recommend_endpoint_returns_recommendations():
    client = TestClient(app)

    response = client.post("/recommend", json={"prompt": "happy pop workout songs"})

    assert response.status_code == 200
    data = response.json()
    assert data["prompt"] == "happy pop workout songs"
    assert data["recommendations"][0]["song"]["title"] == "Sunrise City"
    assert "message" not in data


def test_fastapi_recommend_endpoint_rejects_empty_prompt():
    client = TestClient(app)

    response = client.post("/recommend", json={"prompt": "   "})

    assert response.status_code == 400
    assert "non-empty" in response.json()["detail"]
