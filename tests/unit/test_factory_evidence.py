"""Regression checks for the CF-02A evidence boundary (raw + cleaned sources)."""
import json
from pathlib import Path

import pytest

from src.factory import evidence


@pytest.fixture
def raw_video(tmp_path):
    """One synthetic raw whisper JSON with two clean segments."""
    folder = tmp_path / f"data/{evidence.PLAYLIST_ID}"
    folder.mkdir(parents=True)
    payload = {
        "segments": [
            {"id": 0, "start": 0.0, "end": 4.0, "text": " القانون الأول ينص على أن الحجم الثابت "},
            {"id": 1, "start": 4.0, "end": 9.5, "text": " والقانون الثاني يتحدث عن التقريب "},
        ],
        "language": "ar",
    }
    (folder / f"{evidence.VIDEO_ID}_raw.json").write_text(
        json.dumps(payload, ensure_ascii=False), encoding="utf-8"
    )
    return tmp_path


def write_legacy(root, suffix, payload="\"درس قديم مولّد\""):
    folder = root / f"GeminiLongContext/{evidence.PLAYLIST_ID}"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{evidence.VIDEO_ID}{suffix}"
    path.write_text(payload, encoding="utf-8")
    return path


def test_raw_json_and_cleaned_counterparts_are_eligible_teaching_sources():
    assert evidence.eligibility_of("data/p/0Ca8cjsIysc_raw.json") == "teaching_eligible"
    for suffix, role in [
        ("_chapters.json", "chapter_hints"),
        ("_v2_content.json", "legacy_v2_lesson"),
        ("_content.json", "legacy_generated_context"),
        ("_lecture_context.json", "legacy_lecture_context"),
    ]:
        assert evidence.eligibility_of(
            f"GeminiLongContext/p/0Ca8cjsIysc{suffix}"
        ) == "teaching_eligible_cleaned", role


def test_derived_srt_variants_are_never_eligible():
    for suffix in ("_raw.srt", "_postprocess.srt", ".srt"):
        assert evidence.eligibility_of(f"data/p/0Ca8cjsIysc{suffix}") == "not_eligible"


def test_cleaned_source_is_never_a_segment_load(tmp_path):
    cleaned = write_legacy(tmp_path, "_v2_content.json")
    with pytest.raises(evidence.EvidencePolicyError, match="cleaned source"):
        evidence.load_segments_from(cleaned)


def test_raw_loader_assigns_stable_ids_and_hashes(raw_video):
    segments = evidence.load_raw_video(raw_video, evidence.PLAYLIST_ID, evidence.VIDEO_ID)
    assert [s.ref.segment_id for s in segments] == [
        f"{evidence.VIDEO_ID}:seg:0000",
        f"{evidence.VIDEO_ID}:seg:0001",
    ]
    assert all(s.text_sha256 and s.ref.start >= 0 for s in segments)
    reloaded = evidence.load_raw_video(raw_video, evidence.PLAYLIST_ID, evidence.VIDEO_ID)
    assert [s.text_sha256 for s in reloaded] == [s.text_sha256 for s in segments]


def test_same_length_semantic_corruption_is_detected(raw_video):
    segments = evidence.load_raw_video(raw_video, evidence.PLAYLIST_ID, evidence.VIDEO_ID)
    flipped = segments[0].text.replace("الثابت", "الخابط")
    assert len(flipped) == len(segments[0].text) and flipped != segments[0].text
    with pytest.raises(evidence.EvidenceIntegrityError, match="hash mismatch"):
        evidence.verify_segment(segments[0], flipped)


def test_correction_requires_evidence_and_derivation():
    with pytest.raises(evidence.EvidencePolicyError, match="evidence"):
        evidence.Correction.new(evidence.VIDEO_ID, f"{evidence.VIDEO_ID}:seg:0000", "نص", None, None)
    with pytest.raises(evidence.EvidencePolicyError, match="derivation"):
        evidence.Correction.new(evidence.VIDEO_ID, f"{evidence.VIDEO_ID}:seg:0000", "نص", "raw @12s", None)


@pytest.mark.parametrize("excerpt", ["", "   ", None])
def test_correction_rejects_empty_original_excerpt(tmp_path, excerpt):
    ledger = evidence.CorrectionLedger(tmp_path / "corrections.json")
    with pytest.raises(evidence.EvidencePolicyError, match="original excerpt"):
        ledger.propose(
            evidence.VIDEO_ID, f"{evidence.VIDEO_ID}:seg:0000", excerpt,
            "replacement", "raw segment 0", "source-based correction",
        )
    assert not ledger.path.exists()


def test_legacy_empty_excerpt_cannot_corrupt_transcript(raw_video, tmp_path):
    ledger = evidence.CorrectionLedger(tmp_path / "corrections.json")
    ledger.records = [{
        "kind": "correction", "correction_id": "c-0001", "disposition": "approved",
        "segment_id": f"{evidence.VIDEO_ID}:seg:0000",
        "original_excerpt": "", "corrected_text": "replacement",
    }]
    segments = evidence.load_raw_video(raw_video, evidence.PLAYLIST_ID, evidence.VIDEO_ID)
    with pytest.raises(evidence.EvidenceIntegrityError, match="original excerpt is empty"):
        evidence.apply_corrections(segments, ledger)


def test_unreviewed_correction_quarantines_instead_of_applying(raw_video, tmp_path):
    ledger = evidence.CorrectionLedger(tmp_path / "corrections.json")
    correction = ledger.propose(
        video_id=evidence.VIDEO_ID,
        segment_id=f"{evidence.VIDEO_ID}:seg:0000",
        original_excerpt="الحجم الثابت",
        corrected_text="الحجم المضبوط",
        evidence_span="raw segment 0 @0-4s + reviewer audio check",
        derivation="the speaker says المضبوط; the ASR output الثابت is a mishearing",
    )
    segments = evidence.load_raw_video(raw_video, evidence.PLAYLIST_ID, evidence.VIDEO_ID)
    outcome = evidence.apply_corrections(segments, ledger)
    assert outcome.applied == []
    assert outcome.quarantined == [correction["correction_id"]]
    assert outcome.texts[0] == segments[0].text


def test_reviewer_approval_applies_correction_and_is_append_only(raw_video, tmp_path):
    ledger_path = tmp_path / "corrections.json"
    ledger = evidence.CorrectionLedger(ledger_path)
    correction = ledger.propose(
        video_id=evidence.VIDEO_ID,
        segment_id=f"{evidence.VIDEO_ID}:seg:0000",
        original_excerpt="الحجم الثابت",
        corrected_text="الحجم المضبوط",
        evidence_span="raw segment 0 @0-4s",
        derivation="speaker audio says المضبوط",
    )
    with pytest.raises(evidence.EvidencePolicyError, match="append-only"):
        ledger.rewrite(correction["correction_id"], {"corrected_text": "تلاعب"})
    ledger.record_disposition(correction["correction_id"], reviewer="د. المراجع", decision="approved")
    segments = evidence.load_raw_video(raw_video, evidence.PLAYLIST_ID, evidence.VIDEO_ID)
    outcome = evidence.apply_corrections(segments, ledger)
    assert outcome.applied == [correction["correction_id"]]
    assert outcome.quarantined == []
    assert "الحجم المضبوط" in outcome.texts[0]
    reloaded = evidence.CorrectionLedger(ledger_path)
    assert reloaded.approved_ids() == {correction["correction_id"]}
    # Reading derived state must not rewrite original records on a later save.
    reloaded.record_disposition(correction["correction_id"], reviewer="د. المراجع", decision="rejected")
    persisted = json.loads(ledger_path.read_text(encoding="utf-8"))["records"]
    assert persisted[0]["disposition"] == "proposed"
    assert [record["decision"] for record in persisted[1:]] == ["approved", "rejected"]
    assert evidence.CorrectionLedger(ledger_path).approved_ids() == set()


def test_coverage_validation_uses_references_not_counts(raw_video):
    segments = evidence.load_raw_video(raw_video, evidence.PLAYLIST_ID, evidence.VIDEO_ID)
    with pytest.raises(evidence.EvidenceIntegrityError, match="unknown segment"):
        evidence.validate_coverage(segments, [f"{evidence.VIDEO_ID}:seg:0009"])
    result = evidence.validate_coverage(segments, [f"{evidence.VIDEO_ID}:seg:0000", f"{evidence.VIDEO_ID}:seg:0000"])
    assert result.covered == {f"{evidence.VIDEO_ID}:seg:0000"}
    assert result.uncovered == [f"{evidence.VIDEO_ID}:seg:0001"]
    assert result.total_references == 2  # references, not equal counts


def test_diagram_binding_creates_new_revision_and_requires_review(tmp_path):
    store = evidence.DiagramStore(tmp_path / "diagrams.json")
    revision = store.bind(
        video_id=evidence.VIDEO_ID,
        timestamp=300.0,
        capture_sha256="a" * 64,
        captured_at="2026-09-06T00:00:00+00:00",
    )
    assert revision["revision_id"] == "d-0001"
    assert revision["status"] == "pending_review"
    with pytest.raises(evidence.EvidenceIntegrityError, match="immutable"):
        store.bind(
            video_id=evidence.VIDEO_ID,
            timestamp=300.0,
            capture_sha256="b" * 64,
            captured_at="2026-09-06T00:00:00+00:00",
            revision_id=revision["revision_id"],
        )
    replacement = store.bind(
        video_id=evidence.VIDEO_ID,
        timestamp=300.5,
        capture_sha256="b" * 64,
        captured_at="2026-09-06T01:00:00+00:00",
        replaces=revision["revision_id"],
    )
    assert replacement["revision_id"] == "d-0002"
    assert replacement["replaces"] == revision["revision_id"]
    with pytest.raises(evidence.EvidencePolicyError, match="reviewer"):
        store.approve(replacement["revision_id"], reviewer=None)
    store.approve(replacement["revision_id"], reviewer="د. المراجع")
    assert store.get(replacement["revision_id"])["status"] == "approved"


def test_evidence_index_covers_all_available_raw_sets(tmp_path):
    folder = tmp_path / f"data/{evidence.PLAYLIST_ID}"
    folder.mkdir(parents=True)
    for vid in ("AAAAAAAAAAA", "BBBBBBBBBBB"):
        payload = {"segments": [{"id": 0, "start": 0.0, "end": 1.0, "text": "نص"}]}
        (folder / f"{vid}_raw.json").write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    (folder / f"{evidence.VIDEO_ID}_raw.srt").write_text("1\n00:00:00,000 --> 00:00:01,000\nx\n", encoding="utf-8")
    index = evidence.build_evidence_index(tmp_path)
    assert set(index["videos"]) == {"AAAAAAAAAAA", "BBBBBBBBBBB"}
    assert index["videos"]["AAAAAAAAAAA"]["segment_count"] == 1
    assert index["non_raw_skipped"] == [f"{evidence.VIDEO_ID}_raw.srt"]
    assert index["policy"] == (
        "raw whisper JSON is the segment source; cleaned GeminiLongContext counterparts "
        "are video-level teaching sources; derived SRT variants are never authoring inputs"
    )
