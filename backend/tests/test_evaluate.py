import pytest

from app.agent import MusicCuratorAgent
from app.evaluate import (
    EXPECTED_TRACE_STEPS,
    EvaluationCase,
    default_evaluation_cases,
    main,
    run_case,
)


def test_default_evaluation_cases_can_be_loaded():
    cases = default_evaluation_cases()

    assert len(cases) == 8
    assert all(case.prompt for case in cases)
    assert all(case.expected_trace_steps == EXPECTED_TRACE_STEPS for case in cases)


def test_known_good_case_passes():
    agent = MusicCuratorAgent()
    case = default_evaluation_cases()[0]

    result = run_case(agent, case)

    assert result.passed is True
    assert result.failures == []
    assert result.top_song == "Sunrise City"


def test_default_evaluation_cases_have_valid_confidence_scores():
    agent = MusicCuratorAgent()

    for case in default_evaluation_cases():
        result = run_case(agent, case)
        assert 0.0 <= result.confidence_score <= 1.0


def test_wrong_expected_top_song_fails():
    agent = MusicCuratorAgent()
    case = EvaluationCase(
        name="bad_expectation",
        prompt="happy pop workout songs",
        expected_confidence_labels={"high"},
        expected_requires_human_review=False,
        expected_trace_steps=EXPECTED_TRACE_STEPS,
        expected_top_song="Not A Real Top Song",
    )

    result = run_case(agent, case)

    assert result.passed is False
    assert any("top song" in failure for failure in result.failures)


def test_main_exits_successfully_for_default_cases(capsys):
    main()

    output = capsys.readouterr().out
    assert "Passed 8/8 evaluation cases" in output
    assert "[FAIL]" not in output
