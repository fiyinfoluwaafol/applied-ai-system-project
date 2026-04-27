from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Set

from app.agent import MusicCuratorAgent


EXPECTED_TRACE_STEPS = [
    "intent_parser",
    "retriever",
    "scorer",
    "explainer",
    "confidence",
    "guardrails",
]


@dataclass(frozen=True)
class EvaluationCase:
    name: str
    prompt: str
    expected_confidence_labels: Set[str]
    expected_requires_human_review: bool
    expected_trace_steps: Sequence[str]
    expected_top_song: Optional[str] = None
    allow_guardrail_warnings: bool = False


@dataclass(frozen=True)
class EvaluationResult:
    case: EvaluationCase
    passed: bool
    failures: List[str]
    confidence_label: str
    confidence_score: float
    requires_human_review: bool
    top_song: Optional[str]
    warning_count: int


def default_evaluation_cases() -> List[EvaluationCase]:
    return [
        EvaluationCase(
            name="strong_pop_workout",
            prompt="happy pop workout songs",
            expected_confidence_labels={"high"},
            expected_requires_human_review=False,
            expected_trace_steps=EXPECTED_TRACE_STEPS,
            expected_top_song="Sunrise City",
        ),
        EvaluationCase(
            name="synonym_lofi_study",
            prompt="lo-fi study beats to relax",
            expected_confidence_labels={"high"},
            expected_requires_human_review=False,
            expected_trace_steps=EXPECTED_TRACE_STEPS,
            expected_top_song="Library Rain",
        ),
        EvaluationCase(
            name="medium_sad_hip_hop",
            prompt="sad hip hop songs",
            expected_confidence_labels={"medium"},
            expected_requires_human_review=False,
            expected_trace_steps=EXPECTED_TRACE_STEPS,
        ),
        EvaluationCase(
            name="folk_acoustic_warning_allowed",
            prompt="quiet acoustic folk coffee shop",
            expected_confidence_labels={"medium"},
            expected_requires_human_review=False,
            expected_trace_steps=EXPECTED_TRACE_STEPS,
            allow_guardrail_warnings=True,
        ),
        EvaluationCase(
            name="party_house",
            prompt="party house tracks",
            expected_confidence_labels={"medium", "high"},
            expected_requires_human_review=False,
            expected_trace_steps=EXPECTED_TRACE_STEPS,
            expected_top_song="Neon Basement",
        ),
        EvaluationCase(
            name="low_calm_sleep",
            prompt="calm sleep music",
            expected_confidence_labels={"low"},
            expected_requires_human_review=True,
            expected_trace_steps=EXPECTED_TRACE_STEPS,
            allow_guardrail_warnings=True,
        ),
        EvaluationCase(
            name="vague_playlist",
            prompt="playlist please",
            expected_confidence_labels={"low"},
            expected_requires_human_review=True,
            expected_trace_steps=EXPECTED_TRACE_STEPS,
            allow_guardrail_warnings=True,
        ),
        EvaluationCase(
            name="nonsense_prompt",
            prompt="asdf qwer zzzz",
            expected_confidence_labels={"low"},
            expected_requires_human_review=True,
            expected_trace_steps=EXPECTED_TRACE_STEPS,
            allow_guardrail_warnings=True,
        ),
    ]


def run_case(agent: MusicCuratorAgent, case: EvaluationCase) -> EvaluationResult:
    failures: List[str] = []

    try:
        response = agent.run(case.prompt)
    except Exception as error:
        return EvaluationResult(
            case=case,
            passed=False,
            failures=[f"agent raised {type(error).__name__}: {error}"],
            confidence_label="error",
            confidence_score=0.0,
            requires_human_review=False,
            top_song=None,
            warning_count=0,
        )

    recommendations = response.get("recommendations", [])
    confidence = response.get("confidence", {})
    guardrails = response.get("guardrails", {})
    trace = response.get("trace", [])

    confidence_label = str(confidence.get("label", "missing"))
    confidence_score = confidence.get("score")
    requires_review = bool(guardrails.get("requires_human_review", False))
    warnings = guardrails.get("warnings", [])
    top_song = recommendations[0]["song"]["title"] if recommendations else None

    if not recommendations:
        failures.append("no recommendations returned")
    if confidence_label not in case.expected_confidence_labels:
        expected = ", ".join(sorted(case.expected_confidence_labels))
        failures.append(f"confidence label '{confidence_label}' not in expected {{{expected}}}")
    if not isinstance(confidence_score, (int, float)) or not 0.0 <= confidence_score <= 1.0:
        failures.append(f"confidence score {confidence_score!r} is not between 0.0 and 1.0")
        confidence_score = 0.0
    if requires_review != case.expected_requires_human_review:
        failures.append(
            "requires_human_review "
            f"{requires_review} != expected {case.expected_requires_human_review}"
        )

    trace_steps = [step.get("step") for step in trace]
    if trace_steps != list(case.expected_trace_steps):
        failures.append(f"trace steps {trace_steps} != expected {list(case.expected_trace_steps)}")
    if any(step.get("status") != "ok" for step in trace):
        failures.append("one or more trace statuses were not ok")

    if case.expected_top_song and top_song != case.expected_top_song:
        failures.append(f"top song '{top_song}' != expected '{case.expected_top_song}'")
    if warnings and not case.allow_guardrail_warnings:
        failures.append(f"unexpected guardrail warnings: {warnings}")

    return EvaluationResult(
        case=case,
        passed=not failures,
        failures=failures,
        confidence_label=confidence_label,
        confidence_score=float(confidence_score),
        requires_human_review=requires_review,
        top_song=top_song,
        warning_count=len(warnings),
    )


def run_evaluation(cases: Iterable[EvaluationCase]) -> List[EvaluationResult]:
    agent = MusicCuratorAgent()
    return [run_case(agent, case) for case in cases]


def print_summary(results: Sequence[EvaluationResult]) -> None:
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(
            f"[{status}] {result.case.name}: "
            f"confidence={result.confidence_label} ({result.confidence_score:.2f}), "
            f"review={result.requires_human_review}, "
            f"top={result.top_song or 'none'}, "
            f"warnings={result.warning_count}"
        )
        for failure in result.failures:
            print(f"  - {failure}")

    passed = sum(1 for result in results if result.passed)
    total = len(results)
    print(f"\nPassed {passed}/{total} evaluation cases")


def main() -> None:
    results = run_evaluation(default_evaluation_cases())
    print_summary(results)
    if any(not result.passed for result in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

