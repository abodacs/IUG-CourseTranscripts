#!/usr/bin/env python3
"""Capture existing JSON keyframe hints from a matching local/YouTube video; no AI."""
import argparse
import hashlib
import html
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

VIDEO_ID = re.compile(r"[A-Za-z0-9_-]{11}")
CAPTURE_VERSION = 1


def sha256(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def seconds(value):
    """Numeric timestamps are seconds; accept MM:SS or HH:MM:SS too."""
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError("timestamp must be seconds, MM:SS, or HH:MM:SS")
    parts = str(value).strip().replace(",", ".").split(":")
    if not 1 <= len(parts) <= 3:
        raise ValueError(f"invalid timestamp: {value!r}")
    try:
        nums = [float(part) for part in parts]
    except ValueError:
        raise ValueError(f"invalid timestamp: {value!r}") from None
    if any(not math.isfinite(n) or n < 0 for n in nums):
        raise ValueError(f"invalid timestamp: {value!r}")
    if len(nums) > 1 and (any(n >= 60 for n in nums[1:]) or any(n != int(n) for n in nums[:-1])):
        raise ValueError(f"invalid clock timestamp: {value!r}")
    total = sum(n * 60 ** i for i, n in enumerate(reversed(nums)))
    if not math.isfinite(total):
        raise ValueError("timestamp exceeds supported range")
    return total


def load_plan(path, all_candidates=False, offsets=(0.0,)):
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError("video JSON must be an object")
    match = re.fullmatch(r"([A-Za-z0-9_-]{11})(?:_chapters|_v2_content|_raw)?", path.stem)
    inferred = match.group(1) if match else None
    video_id = data.get("video_id", inferred)
    if not isinstance(video_id, str) or not VIDEO_ID.fullmatch(video_id):
        raise ValueError("provide video_id in JSON or use <video_id>_chapters.json")
    if inferred and inferred != video_id:
        raise ValueError("video_id disagrees with the JSON filename")
    chapters = data.get("chapters", [])
    if not isinstance(chapters, list):
        raise ValueError("chapters must be a list")
    moments = []
    for index, chapter in enumerate(chapters):
        if not isinstance(chapter, dict):
            raise ValueError(f"chapter {index + 1} must be an object")
        candidates = chapter.get("candidates_keyframes", [])
        if not isinstance(candidates, list):
            raise ValueError(f"chapter {index + 1}: candidates_keyframes must be a list")
        chosen = chapter.get("chosen_keyframe")
        selected = candidates if all_candidates else ([chosen] if chosen is not None else candidates[:1])
        if all_candidates and chosen is not None:
            selected = [chosen, *candidates]
        for item in selected:
            moments.append((f"chapters[{index}]", chapter, item))
    key_moments = data.get("key_moments", [])
    if not isinstance(key_moments, list):
        raise ValueError("key_moments must be a list")
    moments.extend((f"key_moments[{i}]", {}, item) for i, item in enumerate(key_moments))
    frames, warnings = {}, []
    for location, chapter, item in moments:
        if not isinstance(item, dict) or "timestamp" not in item:
            raise ValueError(f"{location}: keyframe requires a timestamp")
        timestamp = seconds(item["timestamp"])
        hint = {"location": location, "chapter": str(chapter.get("title", "")),
                "description": str(item.get("description", "")), "hint_seconds": timestamp}
        if "start_timestamp" in chapter and "end_timestamp" in chapter:
            start, end = seconds(chapter["start_timestamp"]), seconds(chapter["end_timestamp"])
            if end <= start or not start <= timestamp <= end:
                warning = f"{location}: hint at {timestamp:g}s is outside its chapter range ({start:g}–{end:g}s)"
                warnings.append(warning)
                hint["warning"] = warning
        for offset in offsets:
            requested = timestamp + offset
            if not math.isfinite(requested):
                raise ValueError("capture timestamp exceeds supported range")
            if requested < 0:
                warnings.append(f"{location}: skipped negative offset capture at {requested:g}s")
                continue
            ms = round(requested * 1000)
            frame = frames.setdefault(ms, {"timestamp_ms": ms, "hints": []})
            if hint not in frame["hints"]:
                frame["hints"].append(hint)
    if not frames:
        raise ValueError("no capture hints found; use *_chapters.json or key_moments with timestamps")
    return {"video_id": video_id, "metadata_path": str(path.resolve()),
            "metadata_sha256": sha256(path), "warnings": sorted(set(warnings)),
            "frames": [frames[ms] for ms in sorted(frames)]}


def run_command(command, timeout, label):
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        raise ValueError(f"{label} timed out after {timeout:g}s") from None
    except FileNotFoundError:
        raise ValueError(f"{command[0]} is unavailable") from None
    if result.returncode:
        # Keep signed media URLs and possible credentials out of logs/manifests.
        detail = result.stderr.strip().splitlines()
        message = detail[-1] if detail else "no diagnostic output"
        message = re.sub(r"https?://\S+", "[media URL]", message)[:300]
        raise ValueError(f"{label} failed: {message}")
    return result.stdout


def resolve_source(video_id, video, timeout):
    if video is not None:
        path = video.resolve(strict=True)
        info = json.loads(run_command(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                      "-of", "json", str(path)], timeout, "video probe"))
        return str(path), [], {"kind": "local", "path": str(path), "sha256": sha256(path),
                              "duration": seconds(info["format"]["duration"])}
    url = f"https://www.youtube.com/watch?v={video_id}"
    raw = run_command([sys.executable, "-m", "yt_dlp", "--ignore-config", "--no-playlist",
                       "--no-warnings", "--socket-timeout", "20", "--retries", "2",
                       "--format", "bestvideo[height<=1080][ext=mp4]/best[height<=1080]/bestvideo/best",
                       "--dump-single-json", "--skip-download", url], timeout, "YouTube lookup")
    info = json.loads(raw)
    if info.get("id") != video_id or not isinstance(info.get("url"), str):
        raise ValueError("YouTube lookup did not return this video's playable stream")
    if not info["url"].startswith(("https://", "http://")) or info.get("is_live"):
        raise ValueError("a finite HTTP video stream is required")
    headers = []
    for key in ("User-Agent", "Referer", "Origin"):
        value = str(info.get("http_headers", {}).get(key, ""))
        if "\r" in value or "\n" in value:
            raise ValueError("invalid media request header")
        if value:
            headers.append(f"{key}: {value}\r\n")
    options = ["-rw_timeout", "20000000"]
    if headers:
        options += ["-headers", "".join(headers)]
    return info["url"], options, {"kind": "youtube", "url": url,
                                "format_id": str(info.get("format_id", "")),
                                "duration": seconds(info.get("duration"))}


def capture_frame(source, options, timestamp, target, timeout):
    fd, temp = tempfile.mkstemp(suffix=".png", prefix="capture-", dir=target.parent)
    os.close(fd)
    try:
        run_command(["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", *options,
                     "-ss", f"{timestamp:.3f}", "-i", source, "-map", "0:v:0", "-frames:v", "1",
                     "-update", "1", "-y", temp], timeout, "frame capture")
        with open(temp, "rb") as image:
            if image.read(8) != b"\x89PNG\r\n\x1a\n" or os.path.getsize(temp) < 33:
                raise ValueError("frame capture produced no PNG (check timestamp/video duration)")
        os.replace(temp, target)
    finally:
        Path(temp).unlink(missing_ok=True)


def atomic_write(path, text):
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix="write-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as handle:
            handle.write(text)
        os.replace(temp, path)
    finally:
        Path(temp).unlink(missing_ok=True)


def write_report(folder, manifest):
    atomic_write(folder / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    escape = html.escape
    cards = []
    for frame in manifest["frames"]:
        timestamp = frame["timestamp_ms"] / 1000
        link = f'https://www.youtube.com/watch?v={manifest["video_id"]}&t={int(timestamp)}s'
        image = ""
        if frame["status"] == "captured":
            image = f'<a href="{frame["file"]}"><img loading="lazy" src="{frame["file"]}" alt="Unreviewed video capture at {timestamp:g} seconds"></a>'
        descriptions = "".join(f'<p dir="auto">{escape(h["chapter"])} — {escape(h["description"])}</p>' for h in frame["hints"])
        error = escape(frame.get("error", ""))
        cards.append(f'<article><h2><a href="{link}">{timestamp:g}s</a> · {frame["status"]}</h2>{image}{descriptions}<p>{error}</p></article>')
    warnings = "".join(f"<li>{escape(w)}</li>" for w in manifest["warnings"])
    document = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Capture review — {escape(manifest['video_id'])}</title>
<style>body{{font:16px system-ui;max-width:1200px;margin:2rem auto;padding:0 1rem;color:#202020;background:#fafafa}}main{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:1rem}}article{{padding:1rem;background:white;border:1px solid #ddd;border-radius:8px}}img{{width:100%;height:auto}}h2{{font-size:1rem}}a{{color:#164fa3}}</style>
<h1>Review {escape(manifest['video_id'])}</h1><p>Every capture is unreviewed. Descriptions are JSON hints, not verified image captions. Check the image before using it in a lesson.</p>
<ul>{warnings}</ul><main>{''.join(cards)}</main></html>
'''
    atomic_write(folder / "index.html", document)


def capture_plan(plan, output, video=None, refresh=False, timeout=90):
    folder = output / plan["video_id"]
    folder.mkdir(parents=True, exist_ok=True)
    previous = {}
    manifest_path = folder / "manifest.json"
    if manifest_path.exists():
        try:
            previous = json.loads(manifest_path.read_text())
            if not isinstance(previous, dict):
                previous = {}
        except (ValueError, OSError):
            pass
    if not isinstance(previous.get("frames", []), list):
        previous = {}
    previous_frames = {f["timestamp_ms"]: f for f in previous.get("frames", []) if isinstance(f, dict) and isinstance(f.get("timestamp_ms"), int)}
    identity = {"kind": "local", "sha256": sha256(video)} if video else {"kind": "youtube", "video_id": plan["video_id"]}
    reusable = not refresh and previous.get("source_identity") == identity and previous.get("capture_version") == CAPTURE_VERSION
    frames = [dict(f, status="pending", review_status="unreviewed", file=f'{f["timestamp_ms"]:010d}.png') for f in plan["frames"]]
    manifest = dict(plan, schema_version=1, capture_version=CAPTURE_VERSION, source_identity=identity, frames=frames)
    manifest["source"] = previous.get("source") if reusable else None
    source = None
    source_error = None
    captured = cached = failed = 0
    for frame in frames:
        target = folder / frame["file"]
        old = previous_frames.get(frame["timestamp_ms"], {})
        if reusable and old.get("status") == "captured" and target.is_file() and old.get("sha256") == sha256(target):
            frame.update(status="captured", sha256=old["sha256"])
            cached += 1
        else:
            try:
                if source_error:
                    raise ValueError(source_error)
                if source is None:
                    try:
                        source, options, metadata = resolve_source(plan["video_id"], video, timeout)
                        manifest["source"] = metadata
                    except (ValueError, OSError, KeyError, TypeError) as exc:
                        source_error = str(exc)
                        raise ValueError(source_error) from None
                timestamp = frame["timestamp_ms"] / 1000
                if timestamp >= manifest["source"]["duration"]:
                    raise ValueError(f"{timestamp:g}s is outside video duration {manifest['source']['duration']:g}s")
                capture_frame(source, options, timestamp, target, timeout)
                frame.update(status="captured", sha256=sha256(target))
                captured += 1
            except (ValueError, OSError) as exc:
                frame.update(status="failed", error=str(exc))
                failed += 1
        write_report(folder, manifest)
    return {"captured": captured, "cached": cached, "failed": failed,
            "errors": sorted({f["error"] for f in frames if "error" in f}),
            "gallery": str(folder / "index.html")}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="one JSON file or a directory of *_chapters.json files")
    parser.add_argument("--output", type=Path, default=Path("artifacts/captures"))
    parser.add_argument("--video", type=Path, help="matching local video; only with one JSON input")
    parser.add_argument("--all-candidates", action="store_true", help="include candidate frames in addition to chosen frames")
    parser.add_argument("--offsets", default="0", help="seconds around each hint, e.g. --offsets=-2,0,2")
    parser.add_argument("--dry-run", action="store_true", help="print plan without network, capture, or output writes")
    parser.add_argument("--refresh", action="store_true", help="recapture even when existing image hashes match")
    parser.add_argument("--timeout", type=float, default=90, help="maximum seconds per lookup/probe/capture")
    parser.add_argument("--max-frames", type=int, default=50, help="maximum planned images for this invocation")
    args = parser.parse_args(argv)
    try:
        offsets = tuple(float(x.strip()) for x in args.offsets.split(","))
        if not offsets or any(not math.isfinite(x) for x in offsets):
            raise ValueError("offsets must be finite numbers")
        if not math.isfinite(args.timeout) or args.timeout <= 0 or args.max_frames <= 0:
            raise ValueError("timeout and max-frames must be positive")
        files = sorted(args.input.rglob("*_chapters.json")) if args.input.is_dir() else [args.input]
        if not files or not all(p.is_file() for p in files):
            raise ValueError("input JSON files were not found")
        if args.video and (len(files) != 1 or not args.video.is_file()):
            raise ValueError("--video requires one JSON input and an existing matching local video")
        plans = [load_plan(p, args.all_candidates, offsets) for p in files]
        if len({p["video_id"] for p in plans}) != len(plans):
            raise ValueError("duplicate video IDs in input directory; run each source variant separately")
        count = sum(len(p["frames"]) for p in plans)
        if count > args.max_frames:
            raise ValueError(f"planned {count} frames exceeds --max-frames {args.max_frames}; narrow input or raise the explicit limit")
        if args.dry_run:
            print(json.dumps({"videos": len(plans), "frames": count, "plans": plans}, ensure_ascii=False, indent=2))
            return 0
        if not shutil.which("ffmpeg") or (args.video and not shutil.which("ffprobe")):
            raise ValueError("install ffmpeg (and ffprobe for local videos) first")
        total_failed = 0
        for plan in plans:
            result = capture_plan(plan, args.output, args.video, args.refresh, args.timeout)
            total_failed += result["failed"]
            print(json.dumps(dict(video_id=plan["video_id"], **result), ensure_ascii=False), flush=True)
        return 1 if total_failed else 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
