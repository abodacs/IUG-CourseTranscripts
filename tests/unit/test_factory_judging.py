"""CF-06 checks: judge harness contract, batching, gating, cache, report."""
import json

import pytest

from src.factory import judging
from src.factory.judging import (
    DispatchBlocked,
    FakeJudge,
    JudgeContractError,
    batch_items_for_lesson,
    ensure_dispatch_allowed,
    parse_judge_response,
    run_judging,
    summarize_verdicts,
    verdict_cache_key,
)


def lesson_document():
    return {
        "nodes": [
            {"node_id": "opto2311:node:intro", "text": "مقدمة"},
            {"node_id": "opto2311:node:law", "text": "قانون"},
        ],
        "quizzes": [
            {"quiz_id": "opto2311:quiz:q1", "owner_node": "opto2311:node:intro"},
        ],
    }


def provenance():
    return {"nodes": {"opto2311:node:intro": {"segments": ["AAAAAAAAAAA:seg:0000"]},
                      "opto2311:node:law": {"segments": ["AAAAAAAAAAA:seg:0001"]}}}


CONTEXT = "الدرس الكامل كنص مرجعي للحكم"


def expected_ids():
    return [item_id for item_id, _kind, _refs in batch_items_for_lesson(lesson_document(), provenance())]


def test_batch_items_cover_nodes_and_quiz_parts():
    ids = expected_ids()
    assert ids == [
        "opto2311:node:intro",
        "opto2311:node:law",
        "opto2311:quiz:q1#choices",
        "opto2311:quiz:q1#answer",
        "opto2311:quiz:q1#rationale",
    ]
    kinds = {kind for _i, kind, _r in batch_items_for_lesson(lesson_document(), provenance())}
    assert "quiz_answer" in kinds and "node" in kinds


def test_missing_id_fails_the_whole_batch():
    response = {item_id: "pass" for item_id in expected_ids()[:-1]}
    with pytest.raises(JudgeContractError, match="missing verdict IDs"):
        parse_judge_response(response, expected_ids())


def test_unknown_id_fails_the_batch():
    response = {**{item_id: "pass" for item_id in expected_ids()}, "rogue:id": "pass"}
    with pytest.raises(JudgeContractError, match="unknown verdict IDs"):
        parse_judge_response(response, expected_ids())


def test_invalid_verdict_value_fails():
    response = {item_id: "excellent" for item_id in expected_ids()}
    with pytest.raises(JudgeContractError, match="invalid verdict"):
        parse_judge_response(response, expected_ids())


@pytest.mark.parametrize("raw", ["not json at all", '{"opto2311:node:intro": "pass"', "[1, 2]"])
def test_malformed_judge_output_fails(raw):
    judge = FakeJudge(raw_response=raw)
    with pytest.raises(JudgeContractError):
        run_judging(lesson_document(), provenance(), judge, lesson_context=CONTEXT)


def test_fake_judge_run_returns_all_verdicts_with_context():
    judge = FakeJudge(replies={"opto2311:node:law": "fail"})
    report = run_judging(lesson_document(), provenance(), judge, lesson_context=CONTEXT)
    assert report["verdicts"]["opto2311:node:law"] == "fail"
    assert report["verdicts"]["opto2311:node:intro"] == "pass"
    assert report["rubric_version"] == judging.RUBRIC_VERSION
    assert judge.calls == 1  # one batch; context passed with it


def test_batching_splits_calls_but_keeps_whole_lesson_context():
    judge = FakeJudge()
    run_judging(lesson_document(), provenance(), judge, lesson_context=CONTEXT, batch_size=2)
    assert judge.calls == 3  # ceil(5 items / 2)


def test_real_judge_without_ledger_is_blocked(tmp_path):
    class RealJudge:
        is_fake = False
        model = "expensive-1"

        def call(self, batch_items, lesson_context):  # pragma: no cover - must never run
            raise AssertionError("real dispatch must be refused")

    with pytest.raises(DispatchBlocked, match="no ledger"):
        run_judging(lesson_document(), provenance(), RealJudge(), lesson_context=CONTEXT)
    from src.factory.ledger import Ledger

    book = Ledger(tmp_path / "spend.sqlite")  # allocation OPEN
    try:
        with pytest.raises(DispatchBlocked, match="real judging refused"):
            run_judging(lesson_document(), provenance(), RealJudge(), lesson_context=CONTEXT, ledger=book)
        ensure_dispatch_allowed(FakeJudge(), None)  # fake/dry always allowed
    finally:
        book.close()


def test_cache_reuses_verdicts_and_keys_track_model_and_context():
    judge = FakeJudge()
    cache = {}
    first = run_judging(lesson_document(), provenance(), judge, lesson_context=CONTEXT, cache=cache)
    assert first["cache_hits"] == []
    second = run_judging(lesson_document(), provenance(), judge, lesson_context=CONTEXT, cache=cache)
    assert len(second["cache_hits"]) == len(expected_ids())
    assert judge.calls == 1  # rerun consumed cache, no second dispatch

    keys = list(first["cache_keys"].values())
    other_model = verdict_cache_key("opto2311:node:intro", "node", [], CONTEXT, model="other-model")
    other_context = verdict_cache_key("opto2311:node:intro", "node", [], "نص مختلف")
    assert other_model not in keys and other_context not in keys
    assert first["cache_keys"]["opto2311:node:intro"] in keys  # stable on rerun


def test_summarize_uses_named_denominators():
    report = {"verdicts": {"a": "pass", "b": "fail", "c": "pass"}, "cache_hits": ["c"]}
    summary = summarize_verdicts(report, known_bad_ids=["c"], known_good_ids=["b"])
    assert summary == {
        "judged_items": 3,
        "failed_items": ["b"],
        "bad_accepted": ["c"],       # known-bad that the judge passed
        "known_bad_total": 1,
        "good_rejected": ["b"],      # known-good that the judge failed
        "known_good_total": 1,
        "cache_hits": 1,
    }
