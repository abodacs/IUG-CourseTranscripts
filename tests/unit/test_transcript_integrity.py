"""Regression checks for chapter coverage and persisted cleaning results."""
import json
from unittest.mock import Mock

import pytest

from src.etl import transcript_chapter_extractor as extractor
from src.etl import transcript_integrity as integrity


def subtitle(identifier, start, end):
    return {"index": identifier, "start": start, "end": end, "text": f"source {identifier}"}


def test_boundary_subtitle_is_preserved_once_with_original_timestamps():
    original = [subtitle(1, 0, 1), subtitle(2, 59, 61), subtitle(3, 119, 120)]
    assigned = integrity.assign_subtitles(original, [(0, 60), (60, 120)])
    assert assigned == [[original[0], original[1]], [original[2]]]
    assert assigned[0][1]["end"] == 61


def test_greatest_overlap_owns_segment():
    original = subtitle(1, 59, 65)
    assert integrity.assign_subtitles([original], [(0, 60), (60, 120)]) == [[], [original]]


@pytest.mark.parametrize("subtitles,intervals,reason", [
    ([subtitle(1, 10, 12)], [(0, 5)], "outside"),
    ([subtitle(1, 1, 2)], [(0, 5), (4, 8)], "overlap"),
    ([subtitle(1, 1, 2), subtitle(1, 2, 3)], [(0, 5)], "Duplicate"),
    ([subtitle(1, 1, float("nan"))], [(0, 5)], "Invalid"),
    ([subtitle(1, 3, 4), subtitle(2, 1, 2)], [(0, 5)], "source order"),
])
def test_ambiguous_coverage_blocks_processing(subtitles, intervals, reason):
    with pytest.raises(ValueError, match=reason):
        integrity.assign_subtitles(subtitles, intervals)


@pytest.fixture
def forbid_models(monkeypatch):
    model = Mock(side_effect=AssertionError("unexpected model call"))
    monkeypatch.setattr(extractor.genai, "GenerativeModel", model)
    return model


def test_resume_returns_saved_cleaned_text_without_model(tmp_path, forbid_models):
    state_path = tmp_path / "state.json"
    state = extractor.ProcessingState(state_path)
    state.save_completed_text("video_ch0", integrity.content_hash("raw"), "cleaned Arabic")
    restored = extractor.ProcessingState(state_path)
    assert extractor.transform_transcript_with_gemini("raw", "video", 0, restored, None) == "cleaned Arabic"
    forbid_models.assert_not_called()


def test_legacy_completion_without_result_blocks_instead_of_returning_raw(tmp_path, forbid_models):
    state = extractor.ProcessingState(tmp_path / "state.json")
    state.mark_completed("video_ch0")
    with pytest.raises(ValueError, match="lacks saved text"):
        extractor.transform_transcript_with_gemini("raw", "video", 0, state, None)
    forbid_models.assert_not_called()


@pytest.mark.parametrize("change", ["source", "version", "text"])
def test_changed_or_corrupt_checkpoint_cannot_be_reused(tmp_path, forbid_models, change):
    state = extractor.ProcessingState(tmp_path / "state.json")
    state.save_completed_text("video_ch0", integrity.content_hash("raw"), "cleaned")
    raw = "different" if change == "source" else "raw"
    if change == "version":
        state.state["completed_results"]["video_ch0"]["cleaning_version"] = "obsolete"
    if change == "text":
        state.state["completed_results"]["video_ch0"]["text"] = "changed"
    with pytest.raises(ValueError, match="stale|corrupt"):
        extractor.transform_transcript_with_gemini(raw, "video", 0, state, None)
    forbid_models.assert_not_called()


def test_corrupt_state_is_preserved_and_blocks_recovery(tmp_path):
    path = tmp_path / "state.json"
    path.write_text("truncated{")
    with pytest.raises(ValueError, match="preserve"):
        extractor.ProcessingState(path)
    assert path.read_text() == "truncated{"


def test_failed_atomic_save_preserves_disk_and_memory(tmp_path, monkeypatch):
    path = tmp_path / "state.json"
    state = extractor.ProcessingState(path)
    state.save_state()
    before = path.read_bytes()
    monkeypatch.setattr(integrity.os, "replace", Mock(side_effect=OSError("disk failure")))
    with pytest.raises(OSError):
        state.save_completed_text("video_ch0", integrity.content_hash("raw"), "cleaned")
    assert path.read_bytes() == before
    assert not state.is_completed("video_ch0")
    assert list(tmp_path.iterdir()) == [path]


@pytest.mark.parametrize("bad_block", ["2\ninvalid\ntext", "2\n00:00:05,000 --> 00:00:04,000\ntext", "2\nmissing text"])
def test_malformed_subtitle_cannot_disappear(bad_block):
    valid = "1\n00:00:00,000 --> 00:00:01,000\nvalid"
    with pytest.raises(ValueError):
        extractor.parse_srt(valid + "\n\n" + bad_block)


def write_video(tmp_path):
    (tmp_path / "video.srt").write_text(
        "1\n00:00:00,000 --> 00:00:01,000\nfirst\n\n"
        "2\n00:00:59,000 --> 00:01:01,000\nboundary\n\n"
        "3\n00:01:01,000 --> 00:01:02,000\nlast\n")
    (tmp_path / "video_chapters.json").write_text(json.dumps({"chapters": [
        {"title": "one", "start_timestamp": "00:00:00", "end_timestamp": "00:01:00"},
        {"title": "two", "start_timestamp": "00:01:00", "end_timestamp": "00:02:00"},
    ]}))


def test_video_rerun_validates_saved_source_coverage_without_cleaning(tmp_path, monkeypatch):
    write_video(tmp_path)
    cleaner = Mock(return_value="cleaned")
    monkeypatch.setattr(extractor, "transform_transcript_with_gemini", cleaner)
    state = extractor.ProcessingState(tmp_path / "state.json")
    assert extractor.process_video("video", tmp_path, state, None)
    output = json.loads((tmp_path / "video_v2_content.json").read_text())
    assert [s["index"] for ch in output["chapters"] for s in ch["source_subtitles"]] == [1, 2, 3]
    cleaner.reset_mock()
    assert extractor.process_video("video", tmp_path, state, None)
    cleaner.assert_not_called()


def test_unverified_output_is_preserved_and_does_not_trigger_paid_repair(tmp_path, monkeypatch):
    write_video(tmp_path)
    output = tmp_path / "video_v2_content.json"
    output.write_text('{"legacy": true}')
    cleaner = Mock(side_effect=AssertionError("unexpected cleaning"))
    monkeypatch.setattr(extractor, "transform_transcript_with_gemini", cleaner)
    with pytest.raises(ValueError, match="unverified"):
        extractor.process_video("video", tmp_path, extractor.ProcessingState(tmp_path / "state.json"), None)
    assert output.read_text() == '{"legacy": true}'
    cleaner.assert_not_called()


def test_interrupted_video_resumes_completed_chapter_without_regeneration(tmp_path, monkeypatch):
    from types import SimpleNamespace
    write_video(tmp_path)
    monkeypatch.setattr(extractor, "GEMINI_API_KEY", "test-only")
    monkeypatch.setattr(extractor.genai, "configure", Mock())
    generate = Mock(side_effect=[SimpleNamespace(text="cleaned first"), KeyboardInterrupt()])
    monkeypatch.setattr(extractor.genai, "GenerativeModel", Mock(return_value=SimpleNamespace(generate_content=generate)))
    limiter = Mock()
    limiter.wait_for_quota.return_value = True
    state_path = tmp_path / "state.json"
    with pytest.raises(KeyboardInterrupt):
        extractor.process_video("video", tmp_path, extractor.ProcessingState(state_path), limiter)
    assert not (tmp_path / "video_v2_content.json").exists()
    generate.reset_mock(side_effect=True)
    generate.return_value = SimpleNamespace(text="cleaned last")
    assert extractor.process_video("video", tmp_path, extractor.ProcessingState(state_path), limiter)
    generate.assert_called_once()
    output = json.loads((tmp_path / "video_v2_content.json").read_text())
    assert [ch["cleaned_transcript_text"] for ch in output["chapters"]] == ["cleaned first", "cleaned last"]


def test_usage_persistence_failure_does_not_retry_successful_provider_call(tmp_path, monkeypatch):
    from types import SimpleNamespace
    monkeypatch.setattr(extractor, "GEMINI_API_KEY", "test-only")
    monkeypatch.setattr(extractor.genai, "configure", Mock())
    generate = Mock(return_value=SimpleNamespace(text="cleaned"))
    monkeypatch.setattr(extractor.genai, "GenerativeModel", Mock(return_value=SimpleNamespace(generate_content=generate)))
    state = extractor.ProcessingState(tmp_path / "state.json")
    monkeypatch.setattr(state, "record_api_call", Mock(side_effect=OSError("disk unavailable")))
    limiter = Mock()
    limiter.wait_for_quota.return_value = True
    with pytest.raises(OSError, match="disk unavailable"):
        extractor.transform_transcript_with_gemini("raw", "video", 0, state, limiter)
    generate.assert_called_once()
    assert not state.is_completed("video_ch0")
