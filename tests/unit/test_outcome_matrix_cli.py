"""Unit checks for scripts/outcome_matrix.py (offline outcome-matrix pass).

Exercises start-window / next / dump / verify / persist against a tmp
fixture corpus laid out like the real tree (data/ + GeminiLongContext/ +
artifacts/opto-2311/), mirroring tests/unit/test_cleaned_store.py.
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[2]))

spec = importlib.util.spec_from_file_location(
    "outcome_matrix", Path(__file__).parents[2] / "scripts/outcome_matrix.py"
)
om = importlib.util.module_from_spec(spec)
spec.loader.exec_module(om)

PLAYLIST = "PL" + "x" * 30 + "-"
VID = "VidA0000001"
VID2 = "VidB0000002"
DATE = "2026-09-07"


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def raw_payload():
    return {
        "segments": [
            {"start": 0.0, "end": 2.5, "text": "alpha beta"},
            {"start": 2.5, "end": 5.0, "text": "gamma delta"},
        ]
    }


def make_repo(tmp_path):
    root = tmp_path
    playlist_dir = root / "data" / PLAYLIST
    playlist_dir.mkdir(parents=True)
    for vid in (VID, VID2):
        (playlist_dir / f"{vid}_raw.json").write_text(json.dumps(raw_payload()), encoding="utf-8")
    glc = root / "GeminiLongContext" / PLAYLIST
    glc.mkdir(parents=True)
    (glc / f"{VID}_chapters.json").write_text(
        json.dumps({"chapters": [{"title": "intro", "start_timestamp": "00:00", "end_timestamp": "00:05"}]}),
        encoding="utf-8",
    )
    (glc / f"{VID}_lecture_context.json").write_text("{'note': 'python literal'}", encoding="utf-8")
    art = root / "artifacts" / "opto-2311"
    art.mkdir(parents=True)
    index = {
        "videos": {
            vid: {
                "segment_count": 2,
                "segments": [
                    {"segment_id": f"{vid}:seg:0000", "start": 0.0, "text_sha256": sha("alpha beta")},
                    {"segment_id": f"{vid}:seg:0001", "start": 2.5, "text_sha256": sha("gamma delta")},
                ],
            }
            for vid in (VID, VID2)
        }
    }
    (art / "evidence-index.json").write_text(json.dumps(index), encoding="utf-8")
    order = {
        "playlist_id": PLAYLIST,
        "order": [
            {"position": 1, "video_id": VID, "title": "Lecture 1", "unavailable": False},
            {"position": 2, "video_id": VID2, "title": "Lecture 2", "unavailable": False},
            {"position": 8, "video_id": "VidSkip008", "title": "unavailable", "unavailable": True},
            {"position": 105, "video_id": "VidExam105", "title": "exam notice", "unavailable": False},
        ],
    }
    (art / "lecture-order.json").write_text(json.dumps(order), encoding="utf-8")
    exposure = {
        "schema": 1,
        "created": DATE,
        "note": "append-only",
        "access_kinds_observed": ["transcript_text_read"],
        "counters": {},
        "events": [],
    }
    (art / "exposure-log.json").write_text(json.dumps(exposure), encoding="utf-8")
    return root


def run(root, *argv, date=DATE):
    # common flags are defined on each subparser, so they go after the command
    om.main([*argv, "--root", str(root), "--playlist", PLAYLIST, "--date", date])


def start_window(root, window=2):
    run(root, "start-window", "--window", str(window))


def valid_draft(position=1, vid=VID, title="Lecture 1"):
    return {
        "video_id": vid,
        "position": position,
        "title": title,
        "outcomes": [
            {
                "outcome_id": f"O-p{position:03d}-01",
                "position": position,
                "video_id": vid,
                "task": "Compute the residual accommodation from the fitted lens power.",
                "cognitive_level": "apply",
                "intended_learner": "first-year optometry student",
                "sufficiency": "supported",
                "required_components": {"explanation": [], "example": [], "practice": [], "transfer_task": []},
                "evidence": [{"segment_id": f"{vid}:seg:0000", "excerpt": "alpha beta"}],
                "prerequisites": ["NONE"],
            }
        ],
    }


def test_start_window_archives_and_resets(tmp_path):
    root = make_repo(tmp_path)
    art = root / "artifacts" / "opto-2311"
    old = dict(om.HEADER, created="2026-09-06", outcomes=[{"outcome_id": "O-p001-01"}], lessons=[{"lesson_id": "L-p001"}])
    (art / "outcome-matrix.json").write_text(json.dumps(old), encoding="utf-8")

    start_window(root)

    archive = json.loads((art / "outcome-matrix-window1.json").read_text(encoding="utf-8"))
    assert archive["outcomes"] == [{"outcome_id": "O-p001-01"}]
    fresh = json.loads((art / "outcome-matrix.json").read_text(encoding="utf-8"))
    assert fresh["outcomes"] == [] and fresh["lessons"] == []
    assert fresh["schema"] == 1 and fresh["created"] == DATE


def test_start_window_refuses_archive_overwrite_without_force(tmp_path):
    root = make_repo(tmp_path)
    art = root / "artifacts" / "opto-2311"
    rows = dict(om.HEADER, outcomes=[{"outcome_id": "x"}], lessons=[])

    (art / "outcome-matrix.json").write_text(json.dumps(rows), encoding="utf-8")
    start_window(root)  # archives rows -> outcome-matrix-window1.json

    (art / "outcome-matrix.json").write_text(json.dumps(rows), encoding="utf-8")
    with pytest.raises(SystemExit):
        start_window(root, window=2)
    run(root, "start-window", "--window", "2", "--force")
    assert json.loads((art / "outcome-matrix-window1.json").read_text(encoding="utf-8"))["outcomes"] == [
        {"outcome_id": "x"}
    ]


def test_next_lists_from_beginning_and_skips_unavailable_and_exam_positions(tmp_path, capsys):
    root = make_repo(tmp_path)
    start_window(root)

    run(root, "next", "--window", "2")

    out = capsys.readouterr().out
    assert "0 position(s) persisted" in out
    assert "2 remaining" in out
    assert f"p001 {VID}" in out
    assert f"p002 {VID2}" in out
    assert "VidSkip008" not in out
    assert "VidExam105" not in out


def test_dump_prints_segments_chapter_hints_and_cleaned_paths(tmp_path, capsys):
    root = make_repo(tmp_path)

    run(root, "dump", VID)

    out = capsys.readouterr().out
    assert "[0000] 0.00-2.50 alpha beta" in out
    assert "[0001] 2.50-5.00 gamma delta" in out
    assert "CLEANED chapters:" in out
    assert "CLEANED lecture_context:" in out
    assert "audit-only" in out
    assert "HINT 00:00-00:05 intro" in out


def test_verify_accepts_valid_rows_and_rejects_bad_excerpt(tmp_path, capsys):
    root = make_repo(tmp_path)
    rows_path = tmp_path / "rows.json"
    rows_path.write_text(json.dumps(valid_draft()), encoding="utf-8")

    run(root, "verify", VID, str(rows_path))
    assert "OK 1 rows" in capsys.readouterr().out

    bad = valid_draft()
    bad["outcomes"][0]["evidence"][0]["excerpt"] = "words that appear nowhere"
    rows_path.write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        run(root, "verify", VID, str(rows_path))
    assert exc.value.code == 1
    assert "excerpt not in" in capsys.readouterr().out


def write_draft(root, draft):
    path = root / "artifacts" / "opto-2311" / "pass-drafts" / f"p{draft['position']:03d}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(draft), encoding="utf-8")
    return path


def test_persist_upserts_appends_window_event_and_is_idempotent(tmp_path):
    root = make_repo(tmp_path)
    start_window(root)
    draft_path = write_draft(root, valid_draft())

    run(root, "persist", str(draft_path), "--window", "2")

    art = root / "artifacts" / "opto-2311"
    matrix = json.loads((art / "outcome-matrix.json").read_text(encoding="utf-8"))
    assert matrix["outcomes"][0]["evidence"] == [f"{VID}:seg:0000"]
    assert matrix["outcomes"][0]["evidence_excerpts"][0]["excerpt"] == "alpha beta"
    assert matrix["outcomes"][0]["drafted_by"] == "session:outcome-matrix-pass-w2"
    assert [l["lesson_id"] for l in matrix["lessons"]] == ["L-p001"]

    log = json.loads((art / "exposure-log.json").read_text(encoding="utf-8"))
    assert [e["id"] for e in log["events"]] == ["exp-matrix-w2-p001"]
    assert log["events"][0]["recorded_by"] == "session:outcome-matrix-pass-w2"
    assert log["events"][0]["access_kind"] == "transcript_text_read"
    assert log["counters"]["events_total"] == 1
    assert log["counters"]["candidate_videos_touched_list"] == [VID]

    run(root, "persist", str(draft_path), "--window", "2")
    log = json.loads((art / "exposure-log.json").read_text(encoding="utf-8"))
    assert len(log["events"]) == 1
    assert log["counters"]["events_total"] == 1


def test_persist_excludes_development_families_from_candidate_counter(tmp_path):
    root = make_repo(tmp_path)
    art = root / "artifacts" / "opto-2311"
    (art / "evaluation-families.json").write_text(
        json.dumps({"development_families": [f"fam-{VID}"]}), encoding="utf-8"
    )
    start_window(root)
    draft_path = write_draft(root, valid_draft())

    run(root, "persist", str(draft_path), "--window", "2")

    log = json.loads((art / "exposure-log.json").read_text(encoding="utf-8"))
    assert log["counters"]["candidate_videos_touched_by_transcript_text"] == 0
    assert log["counters"]["candidate_videos_touched_list"] == []


def test_persist_rejects_prerequisite_at_later_position(tmp_path):
    root = make_repo(tmp_path)
    start_window(root)
    draft = valid_draft()
    draft["outcomes"][0]["prerequisites"] = ["O-p005-01"]
    draft_path = write_draft(root, draft)

    with pytest.raises(SystemExit):
        run(root, "persist", str(draft_path), "--window", "2")
    assert "L-p001" not in (
        (root / "artifacts" / "opto-2311" / "outcome-matrix.json").read_text(encoding="utf-8")
    )


def test_next_advances_after_persist(tmp_path, capsys):
    root = make_repo(tmp_path)
    start_window(root)
    run(root, "persist", str(write_draft(root, valid_draft())), "--window", "2")
    capsys.readouterr()

    run(root, "next", "--window", "2")

    out = capsys.readouterr().out
    assert "1 position(s) persisted" in out
    assert "1 remaining" in out
    assert f"p002 {VID2}" in out
    assert f"p001 {VID}" not in out
