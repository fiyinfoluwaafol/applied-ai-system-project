from typing import Any, Dict, List, Optional

from app.tools.confidence import evaluate_confidence
from app.tools.explainer import explain_recommendations
from app.tools.guardrails import evaluate_guardrails, validate_prompt
from app.tools.intent_parser import parse_intent
from app.tools.retriever import catalog_genres, catalog_moods, retrieve_songs
from app.tools.scorer import clamp_k, score_recommendations


class MusicCuratorAgent:
    def __init__(self, songs: Optional[List[Dict[str, Any]]] = None):
        self.songs = songs if songs is not None else retrieve_songs()
        self.genres = catalog_genres(self.songs)
        self.moods = catalog_moods(self.songs)

    def run(self, prompt: str, k: int = 5) -> Dict[str, Any]:
        validate_prompt(prompt)
        playlist_size = clamp_k(k)
        trace: List[Dict[str, str]] = []

        intent = parse_intent(prompt, self.genres, self.moods)
        trace.append({"step": "intent_parser", "status": "ok"})

        songs = self.songs
        trace.append({"step": "retriever", "status": "ok"})

        scored = score_recommendations(intent, songs, k=playlist_size)
        trace.append({"step": "scorer", "status": "ok"})

        recommendations = explain_recommendations(intent, scored)
        trace.append({"step": "explainer", "status": "ok"})

        confidence = evaluate_confidence(intent, scored)
        trace.append({"step": "confidence", "status": "ok"})

        guardrails = evaluate_guardrails(prompt, intent, confidence, recommendations)
        trace.append({"step": "guardrails", "status": "ok"})

        return {
            "prompt": prompt,
            "intent": intent,
            "recommendations": recommendations,
            "confidence": confidence,
            "guardrails": guardrails,
            "trace": trace,
        }
