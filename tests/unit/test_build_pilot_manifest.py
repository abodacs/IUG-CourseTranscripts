"""CF-01 regression checks for the offline pilot source manifest builder."""
import importlib.util
import json
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "build_pilot_manifest", Path(__file__).parents[2] / "scripts/build_pilot_manifest.py"
)
manifest_tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manifest_tool)

CANONICAL = "PL" + "z" * 31 + "1"
ALIAS = CANONICAL[1:]
OTHER_PLAYLIST = "PL" + "y" * 31 + "2"
VID_FULL = "AAAAAAAAAAA"
VID_BAD = "BBBBBBBBBBB"
VID_SKIPPED = "CCCCCCCCCCC"
VID_SHARED = "DDDDDDDDDDD"
VID_CONFLICT = "EEEEEEEEEEE"

SCHEMA = """
CREATE TABLE playlists (
    id INTEGER PRIMARY KEY, source_id TEXT, title TEXT, skip INTEGER, entries TEXT
);
CREATE TABLE sync_github (
    id INTEGER PRIMARY KEY,
    created_at timestamp default current_timestamp,
    modified_at timestamp default null,
    video_id VARCHAR(64), playlist_id VARCHAR(64),
    downloaded_r2 BOOLEAN, synced BOOLEAN, upload_srt_r2 BOOLEAN, skip BOOLEAN
);
"""

TRUNCATED_ENTRIES = '{"entries": [{"id": "' + VID_FULL + '", "title": "محاضرة'


def srt_timestamp(seconds):
    total_ms = round(seconds * 1000)
    hours, remainder = divmod(total_ms, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1_000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def srt_document(cues):
    blocks = []
    for number, (start, end, text) in enumerate(cues, 1):
        blocks.append(f"{number}\n{srt_timestamp(start)} --> {srt_timestamp(end)}\n{text}\n")
    return "\n".join(blocks)


def whisper_segment(index, start, end, text=None):
    return {
        "id": index,
        "start": start,
        "end": end,
        "text": text if text is not None else f"نص {index}",
        "avg_logprob": -0.2,
        "compression_ratio": 1.2,
        "no_speech_prob": 0.01,
    }


def chapter(start, end, chosen=True):
    return {
        "title": "فصل",
        "start_timestamp": start,
        "end_timestamp": end,
        "chosen_keyframe": {"timestamp": 5.0} if chosen else None,
        "candidates_keyframes": [{"timestamp": 4.0}, {"timestamp": 6.0}] if chosen else [],
    }


@pytest.fixture
def pilot_tree(tmp_path):
    """A synthetic repository: DB + corpus covering every classification."""
    (tmp_path / f"data/{CANONICAL}").mkdir(parents=True)
    (tmp_path / f"GeminiLongContext/{CANONICAL}").mkdir(parents=True)

    raw_json = {"segments": [whisper_segment(0, 0.0, 4.0), whisper_segment(1, 4.0, 8.0)], "language": "ar"}
    raw_srt = srt_document([(0.0, 4.0, "نص 0"), (4.0, 8.0, "نص 1")])
    (tmp_path / f"data/{CANONICAL}/{VID_FULL}_raw.json").write_text(
        json.dumps(raw_json, ensure_ascii=False), encoding="utf-8"
    )
    (tmp_path / f"data/{CANONICAL}/{VID_FULL}_raw.srt").write_text(raw_srt, encoding="utf-8")
    (tmp_path / f"data/{CANONICAL}/{VID_FULL}_postprocess.srt").write_text(raw_srt, encoding="utf-8")
    (tmp_path / f"data/{CANONICAL}/{VID_FULL}.srt").write_text("\n" + raw_srt, encoding="utf-8")
    (tmp_path / f"GeminiLongContext/{CANONICAL}/{VID_FULL}_chapters.json").write_text(
        json.dumps({"chapters": [chapter("00:00:00", "00:00:08")]}, ensure_ascii=False), encoding="utf-8"
    )
    (tmp_path / f"GeminiLongContext/{CANONICAL}/{VID_FULL}_v2_content.json").write_text(
        json.dumps({"lesson": "legacy"}, ensure_ascii=False), encoding="utf-8"
    )

    bad_segments = [
        whisper_segment(0, 10.0, 8.0),
        whisper_segment(1, 3.0, 5.0),
        whisper_segment(2, 20.0, 22.0, "نص 2"),
        whisper_segment(3, 20.0, 22.0, "نص 2"),
        whisper_segment(4, 15.0, 16.0),
        whisper_segment(5, 40.0, 40.0),
    ]
    (tmp_path / f"data/{CANONICAL}/{VID_BAD}_raw.json").write_text(
        json.dumps({"segments": bad_segments}, ensure_ascii=False), encoding="utf-8"
    )
    broken_srt = (
        srt_document([(0.0, 2.0, "سطر")])
        + "\n2\nليس طابع زمني\nنص تالف\n\n3\n00:00:30,000 --> 00:00:20,000\nمعكوس\n\n"
        + srt_document([(60.0, 60.0, "صفري"), (120.0, 125.0, "كرر"), (120.0, 125.0, "كرر بصيغة مختلفة")])
    )
    (tmp_path / f"data/{CANONICAL}/{VID_BAD}_raw.srt").write_text(broken_srt, encoding="utf-8")
    (tmp_path / f"data/{CANONICAL}/{VID_BAD}_postprocess.srt").write_text(
        srt_document([(0.0, 4.0, "معدل")]), encoding="utf-8"
    )

    conflicting = {"segments": [whisper_segment(0, 0.0, 2.0, "نسخة مختلفة")], "language": "ar"}
    (tmp_path / f"GeminiLongContext/{CANONICAL}/{VID_CONFLICT}_raw.json").write_text(
        json.dumps(conflicting, ensure_ascii=False), encoding="utf-8"
    )
    (tmp_path / f"data/{CANONICAL}/{VID_CONFLICT}_raw.json").write_text(
        json.dumps({"segments": [whisper_segment(0, 0.0, 9.0)]}, ensure_ascii=False), encoding="utf-8"
    )

    alias_dir = tmp_path / f"data/{ALIAS}"
    alias_dir.mkdir()
    (alias_dir / f"{VID_SHARED}_raw.json").write_text(
        json.dumps({"segments": [whisper_segment(0, 0.0, 3.0)]}, ensure_ascii=False), encoding="utf-8"
    )

    playlists = [
        (CANONICAL, "بصريات تجريبية", None, TRUNCATED_ENTRIES),
        (OTHER_PLAYLIST, "مسار آخر", None, "[]"),
    ]
    rows = [
        (VID_FULL, ALIAS, 1, None, "2024-08-31 15:21:57"),
        (VID_BAD, CANONICAL, 1, None, "2024-08-31 15:22:10"),
        (VID_SKIPPED, CANONICAL, 0, 1, "2024-08-31 15:22:20"),
        (VID_SHARED, ALIAS, 1, None, "2024-08-31 15:22:30"),
        (VID_SHARED, OTHER_PLAYLIST, 1, None, "2024-08-31 15:22:31"),
        (VID_CONFLICT, CANONICAL, 1, None, "2024-08-31 15:22:31"),
    ]
    conn = sqlite3.connect(tmp_path / "youtube-iug.db")
    conn.executescript(SCHEMA)
    conn.executemany(
        "INSERT INTO playlists (source_id, title, skip, entries) VALUES (?, ?, ?, ?)", playlists
    )
    conn.executemany(
        "INSERT INTO sync_github (video_id, playlist_id, downloaded_r2, skip, created_at) VALUES (?, ?, ?, ?, ?)",
        rows,
    )
    conn.commit()
    conn.close()
    return tmp_path


def build(pilot_tree, playlist=CANONICAL):
    return manifest_tool.build_semantic_manifest(pilot_tree, playlist)


def video(semantic, video_id):
    return next(v for v in semantic["videos"] if v["video_id"] == video_id)


def codes(record):
    return {item["code"] for item in record["integrity"]["findings"]}


def test_alias_membership_resolves_to_canonical_playlist(pilot_tree):
    semantic = build(pilot_tree)
    assert semantic["playlist"]["playlist_id"] == CANONICAL
    assert semantic["playlist"]["membership_count"] == 5
    full = video(semantic, VID_FULL)
    assert full["membership"]["id_form"] == "alias_missing_leading_p"
    assert full["membership"]["recorded_playlist_id"] == ALIAS


def test_files_in_alias_folder_are_discovered_by_video_id(pilot_tree):
    semantic = build(pilot_tree)
    shared = video(semantic, VID_SHARED)
    assert shared["variants"]["raw_transcript_json"][0]["path"] == f"data/{ALIAS}/{VID_SHARED}_raw.json"
    assert shared["shared_video_id"] is True
    assert shared["membership"]["other_playlist_memberships"] == [OTHER_PLAYLIST]


def test_skipped_video_without_raw_stays_visible_and_unresolved(pilot_tree):
    semantic = build(pilot_tree)
    skipped = video(semantic, VID_SKIPPED)
    assert skipped["membership"]["skip"] == 1
    assert skipped["source_gap"] == {"skip_flag": 1, "has_raw_transcript": False, "disposition": "unresolved"}
    blocker_ids = {blocker["id"] for blocker in semantic["blockers"]}
    assert "skipped-source-disposition" in blocker_ids
    assert VID_SKIPPED in next(b for b in semantic["blockers"] if b["id"] == "skipped-source-disposition")["description"]


def test_conflicting_variants_are_kept_separate_and_flagged(pilot_tree):
    semantic = build(pilot_tree)
    conflict = video(semantic, VID_CONFLICT)
    raw_records = conflict["variants"]["raw_transcript_json"]
    assert len(raw_records) == 2
    assert len({record["sha256"] for record in raw_records}) == 2
    item = next(f for f in conflict["integrity"]["findings"] if f["code"] == "conflicting_variants")
    assert item["severity"] == "critical"


def test_identical_duplicate_copies_warn_instead_of_fail(tmp_path):
    (tmp_path / f"data/{CANONICAL}").mkdir(parents=True)
    (tmp_path / f"GeminiLongContext/{CANONICAL}").mkdir(parents=True)
    payload = json.dumps({"segments": [whisper_segment(0, 0.0, 1.0)]}, ensure_ascii=False)
    for folder in (f"data/{CANONICAL}", f"GeminiLongContext/{CANONICAL}"):
        (tmp_path / folder / f"{VID_FULL}_raw.json").write_text(payload, encoding="utf-8")
    conn = sqlite3.connect(tmp_path / "youtube-iug.db")
    conn.executescript(SCHEMA)
    conn.execute(
        "INSERT INTO playlists (source_id, title, skip, entries) VALUES (?, ?, NULL, ?)",
        (CANONICAL, "t", "[]"),
    )
    conn.execute(
        "INSERT INTO sync_github (video_id, playlist_id, downloaded_r2, skip) VALUES (?, ?, 1, NULL)",
        (VID_FULL, CANONICAL),
    )
    conn.commit()
    conn.close()
    semantic = manifest_tool.build_semantic_manifest(tmp_path, CANONICAL)
    item = next(
        f for f in video(semantic, VID_FULL)["integrity"]["findings"] if f["code"] == "conflicting_variants"
    )
    assert item["severity"] == "warning"


def test_malformed_segments_are_flagged_not_silently_normalized(pilot_tree):
    semantic = build(pilot_tree)
    bad = video(semantic, VID_BAD)
    details = " | ".join(
        item["detail"] for item in bad["integrity"]["findings"] if item["code"] == "invalid_segment"
    )
    assert "end<start" in details
    assert "out of order" in details
    assert {"duplicate_segment", "zero_duration_segment"} <= codes(bad)


def test_segment_to_cue_mismatch_is_recorded(pilot_tree):
    semantic = build(pilot_tree)
    bad = video(semantic, VID_BAD)
    assert "count_mismatch" in codes(bad)
    delta = bad["integrity"]["cross_checks"]["raw_json_vs_raw_srt"]["segment_count_delta"]
    assert delta != 0


def test_malformed_srt_blocks_are_flagged(pilot_tree):
    semantic = build(pilot_tree)
    bad = video(semantic, VID_BAD)
    details = " | ".join(
        item["detail"] for item in bad["integrity"]["findings"] if item["code"] == "invalid_cue"
    )
    assert "timestamp line" in details
    assert "end<start" in details
    assert {"zero_duration_cue", "duplicate_timestamp_range"} <= codes(bad)
    srt_findings = [
        item for item in bad["integrity"]["findings"]
        if item["code"] in ("invalid_cue", "zero_duration_cue", "duplicate_timestamp_range")
    ]
    assert srt_findings
    assert {item["variant"] for item in srt_findings} == {"raw_transcript_srt"}


def test_postprocess_fidelity_status_separates_identical_from_unchecked(pilot_tree):
    semantic = build(pilot_tree)
    assert (
        video(semantic, VID_FULL)["integrity"]["postprocess_srt"]["fidelity_status"]
        == "identical_to_raw_srt"
    )
    assert (
        video(semantic, VID_BAD)["integrity"]["postprocess_srt"]["fidelity_status"]
        == "needs_fidelity_check"
    )


def test_cleaned_variants_are_teaching_eligible_srt_variants_are_not(pilot_tree):
    semantic = build(pilot_tree)
    full = video(semantic, VID_FULL)
    assert set(full["eligibility"]["teaching_eligible"]) == {"raw_transcript_json", "raw_transcript_srt"}
    assert set(full["eligibility"]["teaching_eligible_cleaned"]) == {
        "chapter_hints",
        "legacy_v2_lesson",
    }
    assert full["eligibility"]["conditional_fidelity_check"] == ["postprocess_srt"]
    assert full["eligibility"]["classify_only_not_trusted"] == ["normalized_srt"]


def test_truncated_entries_metadata_is_reported_without_invention(pilot_tree):
    semantic = build(pilot_tree)
    entries = semantic["playlist"]["entries_metadata"]
    assert entries["truncated"] is True
    assert entries["format"] == "unparseable"
    assert entries["stored_length"] == len(TRUNCATED_ENTRIES)
    assert "truncated-entries-metadata" in {blocker["id"] for blocker in semantic["blockers"]}


def test_lecture_order_is_unknown_with_batch_import_evidence(pilot_tree):
    semantic = build(pilot_tree)
    order = semantic["playlist"]["order_evidence"]
    assert order["lecture_order"] == "unknown"
    assert order["created_at_span_seconds"] == 34.0
    for record in semantic["videos"]:
        assert record["lecture_order"]["position"] == "unknown"


def test_keyframe_hints_are_counted_from_chapters(pilot_tree):
    semantic = build(pilot_tree)
    hints = video(semantic, VID_FULL)["keyframe_hints"]
    assert hints == {"chapters": 1, "chosen_keyframes": 1, "candidate_timestamps": 2, "range_warnings": 0}


def test_family_watchlist_records_siblings_without_processing(pilot_tree):
    semantic = build(pilot_tree)
    watched = {family["playlist_id"] for family in semantic["family_watchlist"]}
    assert watched == {
        "PL9fwy3NUQKwb_KOrEPbVXCHcPMZKR0uEY",
        "PL9fwy3NUQKwZZYWdO8xTBLJBmEjaQDzzb",
    }
    assert all(family["local_sync_memberships"] == 0 for family in semantic["family_watchlist"])


def test_unchanged_rerun_produces_identical_manifest_hash(pilot_tree):
    first = build(pilot_tree)
    second = build(pilot_tree)
    assert manifest_tool.manifest_hash(first) == manifest_tool.manifest_hash(second)
    document_a = manifest_tool.write_manifest(first, "db-hash", pilot_tree / "a.json")
    document_b = manifest_tool.write_manifest(second, "db-hash", pilot_tree / "b.json")
    assert document_a["manifest_sha256"] == document_b["manifest_sha256"]
    assert "generated_at" in document_a["inspection"]
    assert "generated_at" not in json.dumps(first)


def test_nonempty_wal_refuses_and_leaves_database_untouched(tmp_path):
    (tmp_path / "youtube-iug.db").write_bytes(b"SQLite format 3\x00" + b"\x00" * 32)
    wal = tmp_path / "youtube-iug.db-wal"
    wal.write_bytes(b"pending-writes")
    before = (tmp_path / "youtube-iug.db").read_bytes(), wal.read_bytes()
    with pytest.raises(manifest_tool.ManifestError, match="nonempty WAL"):
        manifest_tool.build_semantic_manifest(tmp_path, CANONICAL)
    after = (tmp_path / "youtube-iug.db").read_bytes(), wal.read_bytes()
    assert before == after


def test_unknown_playlist_is_refused(pilot_tree):
    with pytest.raises(manifest_tool.ManifestError, match="not found"):
        build(pilot_tree, playlist="PLunknownaaaaaaaaaaaaaaaaaaa1")


def test_main_writes_local_manifest_and_reports_blockers(pilot_tree):
    exit_code = manifest_tool.main(
        [
            "--playlist", CANONICAL,
            "--root", str(pilot_tree),
            "--output", str(pilot_tree / "artifacts/opto-2311/source-manifest.json"),
        ]
    )
    assert exit_code == 0
    document = json.loads(
        (pilot_tree / "artifacts/opto-2311/source-manifest.json").read_text(encoding="utf-8")
    )
    assert document["manifest"]["playlist"]["playlist_id"] == CANONICAL
    assert document["manifest"]["summary"]["expected_videos"] == 5
    assert document["manifest"]["blockers"]


@pytest.mark.parametrize("value,expected", [
    (15, 15.0),
    (1.25, 1.25),
    ("13:37", 817.0),
    ("00:13:37", 817.0),
    ("00:00:01,570", 1.57),
    ("01:02:03.500", 3723.5),
])
def test_timestamp_units_accept_srt_chapter_and_float_forms(value, expected):
    assert manifest_tool.timestamp_seconds(value) == pytest.approx(expected)


@pytest.mark.parametrize("value", [-1, True, None, "nan", "inf", "00:99", "1:2:3:4", "1.5:02"])
def test_invalid_timestamp_units_are_rejected(value):
    with pytest.raises(ValueError):
        manifest_tool.timestamp_seconds(value)


def test_module_imports_no_application_or_network_modules():
    script = str(Path(manifest_tool.__file__).resolve())
    probe = (
        "import importlib.util, sys\n"
        f"spec = importlib.util.spec_from_file_location('bpm', r'{script}')\n"
        "module = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(module)\n"
        "banned = {'src', 'requests', 'httpx', 'urllib3', 'google.generativeai', 'google.genai', 'openai', 'anthropic'}\n"
        "loaded = banned & set(sys.modules)\n"
        "assert not loaded, f'banned modules imported: {loaded}'\n"
        "print('clean')\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", probe], capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0, result.stderr
    assert "clean" in result.stdout
