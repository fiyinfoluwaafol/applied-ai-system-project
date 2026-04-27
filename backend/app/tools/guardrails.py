from typing import Any, Dict, List


def validate_prompt(prompt: str) -> None:
    if not prompt or not prompt.strip():
        raise ValueError("Prompt must be a non-empty string.")


def evaluate_guardrails(
    prompt: str,
    intent: Dict[str, Any],
    confidence: Dict[str, Any],
    recommendations: List[Dict[str, Any]],
) -> Dict[str, Any]:
    warnings: List[str] = list(intent.get("warnings", []))

    if len(prompt.strip()) < 3:
        warnings.append("Prompt is too short to capture a clear listening intent.")
    if not intent.get("matched_terms"):
        warnings.append("Prompt did not match supported genres, moods, or energy cues.")
    if confidence.get("label") == "low":
        warnings.append("Recommendation confidence is low; review results before relying on them.")
    if not recommendations:
        warnings.append("No recommendations were produced.")

    warnings = list(dict.fromkeys(warnings))
    requires_human_review = confidence.get("label") == "low" or not intent.get("matched_terms")

    return {
        "safe": bool(recommendations),
        "requires_human_review": requires_human_review,
        "warnings": warnings,
    }

