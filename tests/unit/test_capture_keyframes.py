"""Keyframe reconciliation and real offline FFmpeg capture checks."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess

import pytest

spec = importlib.util.spec_from_file_location("capture_keyframes", Path(__file__).parents[2] / "scripts/capture_keyframes.py")
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)
VIDEO_ID = "abcdefghijk"


def metadata(tmp_path, timestamps=(1, 3), descriptions=None):
    path = tmp_path / f"{VIDEO_ID}_chapters.json"
    chapters = [{"title": "رسم توضيحي", "start_timestamp": "00:00:00", "end_timestamp": "00:00:04",
                 "chosen_keyframe": {"timestamp": t, "description": (descriptions or {}).get(t, "diagram hint")}}
                for t in timestamps]
    path.write_text(json.dumps({"chapters": chapters}, ensure_ascii=False))
    return path


@pytest.mark.parametrize("value,expected", [(15, 15), (1.25, 1.25), ("13:37", 817), ("00:13:37", 817), ("01:02:03.500", 3723.5)])
def test_timestamp_units(value, expected):
    assert capture.seconds(value) == expected


@pytest.mark.parametrize("value", [-1, True, None, "nan", "inf", "00:99", "1:2:3:4", "1.5:02"])
def test_invalid_timestamps_are_rejected(value):
    with pytest.raises(ValueError):
        capture.seconds(value)


def test_chosen_candidates_and_offsets_preserve_hints_without_duplicate_images(tmp_path):
    path = metadata(tmp_path, (1, 1))
    data = json.loads(path.read_text())
    data["chapters"][0]["candidates_keyframes"] = [{"timestamp": 1, "description": "same moment"}, {"timestamp": 5, "description": "later diagram"}]
    path.write_text(json.dumps(data))
    chosen = capture.load_plan(path)
    assert [f["timestamp_ms"] for f in chosen["frames"]] == [1000]
    assert len(chosen["frames"][0]["hints"]) == 2
    all_frames = capture.load_plan(path, True, (-2, 0, 2))
    assert [f["timestamp_ms"] for f in all_frames["frames"]] == [1000, 3000, 5000, 7000]
    assert any("outside" in warning for warning in all_frames["warnings"])
    assert any("negative" in warning for warning in all_frames["warnings"])


def test_invalid_hint_blocks_plan_instead_of_silently_disappearing(tmp_path):
    path = metadata(tmp_path, (1, "bad"))
    with pytest.raises(ValueError):
        capture.load_plan(path)


def test_flat_key_moments_and_identity_mismatch(tmp_path):
    path = tmp_path / "lecture.json"
    path.write_text(json.dumps({"video_id": VIDEO_ID, "key_moments": [{"timestamp": "00:13:37", "description": "diagram"}]}))
    assert capture.load_plan(path)["frames"][0]["timestamp_ms"] == 817000
    wrong_name = tmp_path / "ABCDEFGHIJK_chapters.json"
    wrong_name.write_text(path.read_text())
    with pytest.raises(ValueError, match="disagrees"):
        capture.load_plan(wrong_name)


def test_dry_run_has_no_network_or_writes_and_enforces_frame_limit(tmp_path, monkeypatch, capsys):
    path = metadata(tmp_path)
    output = tmp_path / "captures"
    monkeypatch.setattr(capture, "capture_plan", lambda *a, **k: pytest.fail("capture during dry-run"))
    assert capture.main([str(path), "--output", str(output), "--dry-run"]) == 0
    assert json.loads(capsys.readouterr().out)["frames"] == 2
    assert not output.exists()
    assert capture.main([str(path), "--output", str(output), "--max-frames", "1"]) == 2
    assert not output.exists()


def test_failed_lookup_records_all_frames_and_returns_nonzero(tmp_path, monkeypatch):
    path = metadata(tmp_path)
    calls = []
    def fail(*args):
        calls.append(args)
        raise ValueError("YouTube lookup failed")
    monkeypatch.setattr(capture, "resolve_source", fail)
    monkeypatch.setattr(capture.shutil, "which", lambda name: name)
    output = tmp_path / "captures"
    assert capture.main([str(path), "--output", str(output)]) == 1
    result = json.loads((output / VIDEO_ID / "manifest.json").read_text())
    assert len(calls) == 1
    assert all(f["status"] == "failed" for f in result["frames"])
    assert all(f["review_status"] == "unreviewed" for f in result["frames"])


def test_failed_commands_do_not_persist_signed_stream_urls(monkeypatch):
    monkeypatch.setattr(capture.subprocess, "run", lambda *a, **kw: subprocess.CompletedProcess(a[0], 1, "", "failed https://media.example/file?token=private"))
    with pytest.raises(ValueError) as error:
        capture.run_command(["ffmpeg"], 1, "capture")
    assert "private" not in str(error.value)
    assert "[media URL]" in str(error.value)


@pytest.mark.skipif(not shutil.which("ffmpeg") or not shutil.which("ffprobe"), reason="requires FFmpeg")
def test_real_capture_pixels_partial_failure_and_verified_resume(tmp_path, monkeypatch):
    video = tmp_path / "lecture.mkv"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=red:s=64x48:r=5:d=2",
                    "-f", "lavfi", "-i", "color=c=blue:s=64x48:r=5:d=2", "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v]",
                    "-map", "[v]", "-c:v", "ffv1", str(video)], check=True, timeout=30)
    path = metadata(tmp_path, (1, 3, 10), {1: '<script>alert("x")</script>'})
    source_hash = capture.sha256(video)
    metadata_hash = capture.sha256(path)
    plan = capture.load_plan(path)
    output = tmp_path / "captures"
    result = capture.capture_plan(plan, output, video)
    assert (result["captured"], result["failed"]) == (2, 1)
    folder = output / VIDEO_ID
    for ms, channel in [(1000, 0), (3000, 2)]:
        pixels = subprocess.run(["ffmpeg", "-v", "error", "-i", str(folder / f"{ms:010d}.png"), "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1"], capture_output=True, check=True, timeout=30).stdout
        assert pixels[channel] > 200
        assert pixels[2 - channel] < 30
    manifest = json.loads((folder / "manifest.json").read_text())
    assert "outside video duration" in manifest["frames"][2]["error"]
    page = (folder / "index.html").read_text()
    assert '<script>alert' not in page
    assert '&lt;script&gt;' in page
    assert capture.sha256(video) == source_hash
    assert capture.sha256(path) == metadata_hash
    plan["frames"] = plan["frames"][:2]
    original_resolve = capture.resolve_source
    monkeypatch.setattr(capture, "resolve_source", lambda *a: pytest.fail("unchanged resume must not probe/fetch"))
    resumed = capture.capture_plan(plan, output, video)
    assert (resumed["captured"], resumed["cached"], resumed["failed"]) == (0, 2, 0)
    monkeypatch.setattr(capture, "resolve_source", original_resolve)
    (folder / "0000001000.png").write_bytes(b"corrupt cache")
    repaired = capture.capture_plan(plan, output, video)
    assert (repaired["captured"], repaired["cached"], repaired["failed"]) == (1, 1, 0)
