"""CF-03 checks: outcome-matrix validation and the discovery worksheet."""
import json
from pathlib import Path

import pytest

from src.factory import outcomes


def evidence_index():
    return {
        "videos": {
            "AAAAAAAAAAA": {"segments": [{"segment_id": "AAAAAAAAAAA:seg:0000"}]},
            "BBBBBBBBBBB": {"segments": [{"segment_id": "BBBBBBBBBBB:seg:0000"}]},
        }
    }


def base_outcome(**overrides):
    outcome = {
        "outcome_id": "O-001",
        "task": "حل مسألة عدسة رقيقة",
        "evidence": ["AAAAAAAAAAA:seg:0000"],
        "sufficiency": "supported",
        "prerequisites": [],
    }
    outcome.update(overrides)
    return outcome


def base_matrix(**outcome_overrides):
    return {
        "outcomes": [base_outcome(**outcome_overrides)],
        "lessons": [{"lesson_id": "L-001", "outcome_ids": ["O-001"], "order_position": 1}],
    }


def test_valid_matrix_passes():
    assert outcomes.validate_outcome_matrix(base_matrix(), evidence_index()) == base_matrix()


def test_duplicate_or_missing_ids_rejected():
    matrix = base_matrix()
    matrix["outcomes"].append(base_outcome())
    with pytest.raises(outcomes.MatrixError, match="duplicated"):
        outcomes.validate_outcome_matrix(matrix, evidence_index())
    with pytest.raises(outcomes.MatrixError, match="outcome_id"):
        outcomes.validate_outcome_matrix({"outcomes": [base_outcome(outcome_id=None)], "lessons": []}, evidence_index())


def test_evidence_references_must_resolve_against_the_index():
    with pytest.raises(outcomes.MatrixError, match="unknown to the index"):
        outcomes.validate_outcome_matrix(base_matrix(evidence=["ZZZZZZZZZZZ:seg:0000"]), evidence_index())


def test_diagram_requirement_and_blocker_note():
    with pytest.raises(outcomes.MatrixError, match="video and time range"):
        outcomes.validate_outcome_matrix(base_matrix(sufficiency="needs_youtube_diagram"), evidence_index())
    ok = base_matrix(
        sufficiency="needs_youtube_diagram",
        diagram={"video_id": "AAAAAAAAAAA", "start": 300.0, "end": 320.0},
    )
    outcomes.validate_outcome_matrix(ok, evidence_index())
    with pytest.raises(outcomes.MatrixError, match="blocker"):
        outcomes.validate_outcome_matrix(base_matrix(sufficiency="unsupported"), evidence_index())


def test_unknown_prerequisite_and_cycles_rejected():
    with pytest.raises(outcomes.MatrixError, match="unknown prerequisite"):
        outcomes.validate_outcome_matrix(base_matrix(prerequisites=["O-404"]), evidence_index())
    cycle = {
        "outcomes": [
            base_outcome(outcome_id="O-001", prerequisites=["O-002"]),
            base_outcome(outcome_id="O-002", prerequisites=["O-001"]),
        ],
        "lessons": [
            {"lesson_id": "L-001", "outcome_ids": ["O-001"]},
            {"lesson_id": "L-002", "outcome_ids": ["O-002"]},
        ],
    }
    with pytest.raises(outcomes.MatrixError, match="cycle"):
        outcomes.validate_outcome_matrix(cycle, evidence_index())


def test_lesson_grouping_must_be_prerequisite_closed():
    matrix = {
        "outcomes": [
            base_outcome(outcome_id="O-001"),
            base_outcome(outcome_id="O-002", prerequisites=["O-001"]),
        ],
        "lessons": [
            {"lesson_id": "L-001", "outcome_ids": ["O-002"]},
            {"lesson_id": "L-002", "outcome_ids": ["O-001"]},
        ],
    }
    with pytest.raises(outcomes.MatrixError, match="not in the same or an earlier lesson"):
        outcomes.validate_outcome_matrix(matrix, evidence_index())


def test_outcome_cannot_sit_in_two_lessons():
    matrix = {
        "outcomes": [base_outcome()],
        "lessons": [
            {"lesson_id": "L-001", "outcome_ids": ["O-001"]},
            {"lesson_id": "L-002", "outcome_ids": ["O-001"]},
        ],
    }
    with pytest.raises(outcomes.MatrixError, match="more than one lesson"):
        outcomes.validate_outcome_matrix(matrix, evidence_index())


def test_worksheet_seeds_hints_and_labels_them_audit_only(tmp_path):
    order = {
        "playlist_id": "PLX",
        "order": [
            {"position": 1, "video_id": "AAAAAAAAAAA", "title": "المحاضرة 1", "duration_seconds": 100, "unavailable": False},
            {"position": 2, "video_id": "SAq013FtOLQ", "title": None, "duration_seconds": None, "unavailable": True},
        ],
    }
    (tmp_path / "order.json").write_text(json.dumps(order, ensure_ascii=False))
    (tmp_path / "index.json").write_text(json.dumps(evidence_index(), ensure_ascii=False))
    chapters = tmp_path / "PLX"
    chapters.mkdir()
    (chapters / "AAAAAAAAAAA_chapters.json").write_text(
        json.dumps({"chapters": [{"title": "ثقب الإبرة", "start_timestamp": "00:00", "end_timestamp": "03:00"}]},
                   ensure_ascii=False),
        encoding="utf-8",
    )
    worksheet = outcomes.build_disposition_worksheet(tmp_path / "order.json", tmp_path / "index.json", tmp_path)
    rows = worksheet["lectures"]
    assert rows[0]["discovery_status"] == "draft_pending_review"
    assert rows[0]["hint_topics"][0]["title"] == "ثقب الإبرة"
    assert rows[1]["discovery_status"] == "skipped_unavailable"
    assert "audit-only" in worksheet["policy"]
