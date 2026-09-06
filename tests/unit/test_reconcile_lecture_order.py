"""CF-02 regression checks for lecture-order parsing and reconciliation."""
import importlib.util
import json
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "reconcile_lecture_order", Path(__file__).parents[2] / "scripts/reconcile_lecture_order.py"
)
order_tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(order_tool)

TSV = (
    "001\t3U8quwM9QDg\tبصريات هندسية: المحاضرة 1\t1426\n"
    "002\t4xAHpFxG_gw\tالمحاضرة 2\t1129\n"
    "003\tSAq013FtOLQ\tNA\tNA\n"
    "004\tT12yPtB_D3A\tالتمرين الثاني\t1044\n"
    "005\toRfOWc0gy_Y\tالتمرين الثاني\t1044\n"
)


def manifest_with(*video_ids):
    return {"videos": [{"video_id": vid} for vid in video_ids]}


def test_parse_preserves_positions_and_flags_unavailable():
    order = order_tool.parse_order_tsv(TSV)
    assert [entry["position"] for entry in order] == [1, 2, 3, 4, 5]
    assert order[0]["duration_seconds"] == 1426
    assert order[2]["video_id"] == "SAq013FtOLQ"
    assert order[2]["unavailable"] is True
    assert order[2]["title"] is None and order[2]["duration_seconds"] is None
    assert order[3]["unavailable"] is False


def test_parse_rejects_malformed_lines_and_gap_positions():
    with pytest.raises(ValueError, match="unexpected line"):
        order_tool.parse_order_tsv("1\tabc\ttitle\n")
    with pytest.raises(ValueError, match="non-contiguous"):
        order_tool.parse_order_tsv("1\tabc\ttitle\t10\n3\tdef\tt2\t20\n")
    with pytest.raises(ValueError, match="empty playlist"):
        order_tool.parse_order_tsv("\n")


def test_reconcile_reports_gaps_in_both_directions():
    order = order_tool.parse_order_tsv(TSV)
    recon = order_tool.reconcile(order, manifest_with("3U8quwM9QDg", "T12yPtB_D3A", "XXXXXXXXXXX"))
    assert recon["playlist_entries"] == 5
    assert recon["local_manifest_videos"] == 3
    missing_local = recon["playlist_entries_without_local_raw"]
    assert [entry["video_id"] for entry in missing_local] == ["4xAHpFxG_gw", "SAq013FtOLQ", "oRfOWc0gy_Y"]
    assert recon["local_videos_absent_from_playlist"] == ["XXXXXXXXXXX"]


def test_reconcile_keeps_skipped_entry_visible_with_position():
    order = order_tool.parse_order_tsv(TSV)
    manifest = manifest_with("3U8quwM9QDg", "SAq013FtOLQ")
    manifest["videos"][1]["source_gap"] = {"skip_flag": 1, "has_raw_transcript": False, "disposition": "unresolved"}
    recon = order_tool.reconcile(order, manifest)
    assert recon["skipped_or_gapped_entries"] == [
        {"video_id": "SAq013FtOLQ", "position": 3, "unavailable_at_fetch": True}
    ]


def test_duplicate_title_groups_detect_reuploads():
    order = order_tool.parse_order_tsv(TSV)
    groups = order_tool.duplicate_title_groups(order)
    assert groups == [
        {"title": "التمرين الثاني", "duration_seconds": 1044, "video_ids": ["T12yPtB_D3A", "oRfOWc0gy_Y"]}
    ]


def test_sequence_hints_count_numbered_titles():
    order = order_tool.parse_order_tsv(TSV)
    assert order_tool.numbered_title_count(order) == 4  # NA title excluded


def test_lecture_number_extraction_handles_digits_and_ordinals():
    assert order_tool.lecture_number_in("المحاضرة 12") == {12}
    assert order_tool.lecture_number_in("المحاضرة السادسة بصريات هندسية") == {6}
    # relative references carry no absolute number
    assert order_tool.lecture_number_in("المحاضرة السابقة") == set()
    assert order_tool.lecture_number_in("المحاضرة القادمة") == set()
    assert order_tool.title_lecture_number("بصريات هندسية: المحاضرة 1") == 1
    assert order_tool.title_lecture_number("مقدمة عامة") is None


def test_transcript_conflict_downgrades_position_to_unknown(tmp_path):
    order = order_tool.parse_order_tsv(
        "1\tAAAAAAAAAAA\tالمحاضرة 2\t900\n2\tBBBBBBBBBBB\tالمحاضرة 3\t900\n3\tCCCCCCCCCCC\tالمحاضرة 4\t900\n"
    )
    (tmp_path / "AAAAAAAAAAA_raw.json").write_text(json.dumps(
        {"segments": [{"text": "في المحاضرة الخامسة تحدثنا عن العدسات"}]}, ensure_ascii=False))
    (tmp_path / "BBBBBBBBBBB_raw.json").write_text(json.dumps(
        {"segments": [{"text": "كما رأينا في المحاضرة الثالثة"}]}, ensure_ascii=False))
    order_tool.cross_check_transcript_references(order, tmp_path)
    assert order[0]["order_evidence"]["quality"] == "unknown_transcript_conflict"
    assert "conflict" in order[0]["order_evidence"]
    assert order[1]["order_evidence"]["quality"] == "verified_playlist_and_transcript"
    assert order[2]["order_evidence"]["quality"] == "playlist_title_only"  # no transcript file
    unavailable = order_tool.parse_order_tsv("1\tSAq013FtOLQ\tNA\tNA\n")
    order_tool.cross_check_transcript_references(unavailable, tmp_path)
    assert unavailable[0]["order_evidence"]["quality"] == "unavailable_entry"


def test_build_document_end_to_end():
    manifest = manifest_with("3U8quwM9QDg", "SAq013FtOLQ")
    manifest["videos"][1]["source_gap"] = {"skip_flag": 1}
    document = order_tool.build_document(TSV, manifest, "PLtest", "2026-09-06T00:00:00+00:00")
    assert document["playlist_id"] == "PLtest"
    assert document["fetch"]["fetched_at"] == "2026-09-06T00:00:00+00:00"
    assert "yt-dlp[default]==2026.8.19" in document["fetch"]["tool"]
    assert len(document["order"]) == 5
    assert document["sequence_hints"]["numbered_titles"] == 4
    assert document["reconciliation"]["local_videos_absent_from_playlist"] == []
