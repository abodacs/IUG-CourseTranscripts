"""CF-03: the outcome matrix — schema, validators, and discovery worksheet.

The matrix records promised outcomes with tangible tasks, prerequisite
closure, evidence references that must resolve against the CF-02A evidence
index, and sufficiency status. Discovery drafts may be seeded from legacy
chapter hints, but hints are audit-only pointers: every outcome needs
transcript-span evidence and reviewer approval before the scope freezes.
"""
from pathlib import Path
import json

SUFFICIENCY_VALUES = ("supported", "needs_youtube_diagram", "unsupported")


class MatrixError(ValueError):
    """The matrix violates schema, reference, or prerequisite-closure rules."""


def _require(condition, message):
    if not condition:
        raise MatrixError(message)


def validate_outcome_matrix(matrix, evidence_index):
    """Structural + referential + closure validation of one matrix document."""
    _require(isinstance(matrix.get("outcomes"), list) and matrix["outcomes"], "outcomes[] missing")
    _require(isinstance(matrix.get("lessons"), list), "lessons[] missing")

    known_segments = {
        segment["segment_id"]
        for video in evidence_index.get("videos", {}).values()
        for segment in video.get("segments", [])
    }
    known_outcomes = set()
    for outcome in matrix["outcomes"]:
        oid = outcome.get("outcome_id")
        _require(oid and oid not in known_outcomes, f"outcome_id missing or duplicated: {oid!r}")
        known_outcomes.add(oid)
        _require(bool(outcome.get("task")), f"{oid}: a tangible task statement is required")
        _require(
            outcome.get("sufficiency") in SUFFICIENCY_VALUES,
            f"{oid}: sufficiency must be one of {SUFFICIENCY_VALUES}",
        )
        evidence = outcome.get("evidence") or []
        _require(evidence, f"{oid}: at least one evidence reference is required")
        for ref in evidence:
            _require(ref in known_segments, f"{oid}: evidence segment unknown to the index: {ref}")
        if outcome["sufficiency"] == "needs_youtube_diagram":
            diagram = outcome.get("diagram") or {}
            _require(
                diagram.get("video_id") and diagram.get("start") is not None,
                f"{oid}: needs_youtube_diagram must name the video and time range",
            )
        if outcome["sufficiency"] == "unsupported":
            _require(
                bool(outcome.get("blocker_note")),
                f"{oid}: unsupported outcomes record the blocker instead of silently dropping",
            )

    for outcome in matrix["outcomes"]:
        for prereq in outcome.get("prerequisites") or []:
            _require(prereq in known_outcomes, f"{outcome['outcome_id']}: unknown prerequisite {prereq}")
    _require_acyclic(matrix["outcomes"])

    lesson_order = {}
    for position, lesson in enumerate(matrix["lessons"]):
        lid = lesson.get("lesson_id")
        _require(lid and lid not in lesson_order, f"lesson_id missing or duplicated: {lid!r}")
        lesson_order[lid] = position
    seen = set()
    for lesson in matrix["lessons"]:
        outcome_ids = lesson.get("outcome_ids") or []
        _require(outcome_ids, f"{lesson['lesson_id']}: lesson has no outcomes")
        for oid in outcome_ids:
            _require(oid in known_outcomes, f"{lesson['lesson_id']}: unknown outcome {oid}")
            _require(oid not in seen, f"{oid}: assigned to more than one lesson")
            seen.add(oid)
        by_id = {o["outcome_id"]: o for o in matrix["outcomes"]}
        for oid in outcome_ids:
            for prereq in by_id[oid].get("prerequisites") or []:
                prereq_lessons = [
                    other["lesson_id"] for other in matrix["lessons"] if prereq in (other.get("outcome_ids") or [])
                ]
                _require(
                    prereq_lessons and lesson_order[prereq_lessons[0]] <= lesson_order[lesson["lesson_id"]],
                    f"{lesson['lesson_id']}: prerequisite {prereq} is not in the same or an earlier lesson",
                )
    return matrix


def _require_acyclic(outcomes):
    graph = {o["outcome_id"]: list(o.get("prerequisites") or []) for o in outcomes}
    resolved, stack = set(), set()

    def visit(node):
        if node in resolved:
            return
        _require(node not in stack, f"prerequisite cycle through {node}")
        stack.add(node)
        for prereq in graph.get(node, []):
            visit(prereq)
        stack.discard(node)
        resolved.add(node)

    for node in graph:
        visit(node)


def build_disposition_worksheet(lecture_order_path, evidence_index_path, chapters_dir):
    """One draft row per ordered lecture, seeded from audit-only chapter
    hints. Hint topics are pointers for discovery — never teaching facts."""
    order_doc = json.loads(Path(lecture_order_path).read_text(encoding="utf-8"))
    index = json.loads(Path(evidence_index_path).read_text(encoding="utf-8"))
    chapters_root = Path(chapters_dir) / order_doc["playlist_id"]
    rows = []
    for entry in order_doc["order"]:
        video_id = entry["video_id"]
        hint_topics = []
        hint_path = chapters_root / f"{video_id}_chapters.json"
        if hint_path.exists():
            payload = json.loads(hint_path.read_text(encoding="utf-8"))
            for chapter in payload.get("chapters", []):
                hint_topics.append(
                    {
                        "title": chapter.get("title"),
                        "range": [chapter.get("start_timestamp"), chapter.get("end_timestamp")],
                    }
                )
        rows.append(
            {
                "position": entry["position"],
                "video_id": video_id,
                "title": entry["title"],
                "unavailable": entry["unavailable"],
                "has_raw_evidence": video_id in index["videos"],
                "hint_topics": hint_topics,
                "discovery_status": "skipped_unavailable" if entry["unavailable"] else "draft_pending_review",
            }
        )
    return {
        "playlist_id": order_doc["playlist_id"],
        "policy": (
            "hint topics are audit-only pointers; outcomes require transcript-span "
            "evidence and reviewer approval (CF-03/F05)"
        ),
        "lectures": rows,
    }
