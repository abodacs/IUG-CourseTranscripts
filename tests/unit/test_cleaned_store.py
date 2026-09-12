"""Unit tests for the GeminiLongContext cleaned-source locator."""
from src.etl import cleaned_store

PLAYLIST = "PL9fwy3NUQKwa02NZMGfzb-pxWSdZcGl_-"


def seed_corpus(tmp_path):
    """Three raw videos; cleaned counterparts cover two of them, support dirs present."""
    data = tmp_path / "data" / PLAYLIST
    data.mkdir(parents=True)
    for support in ("raw", "processed", "final"):
        (tmp_path / "data" / support).mkdir()
    (tmp_path / "data" / "raw" / "zzz98765432_raw.json").write_text("{}", encoding="utf-8")
    for video_id in ("abc12345678", "def45678901", "ghi01234567"):
        (data / f"{video_id}_raw.json").write_text("{}", encoding="utf-8")

    cleaned = tmp_path / "GeminiLongContext" / PLAYLIST
    cleaned.mkdir(parents=True)
    for suffix in ("_chapters.json", "_v2_content.json", "_lecture_context.json", "_content.json"):
        (cleaned / f"abc12345678{suffix}").write_text("{}", encoding="utf-8")
    (cleaned / "def45678901_lecture_context.json").write_text("{}", encoding="utf-8")
    return tmp_path


def test_cleaned_path_mirrors_the_raw_tree():
    assert str(cleaned_store.cleaned_path(PLAYLIST, "abc12345678", "chapters")) == (
        f"GeminiLongContext/{PLAYLIST}/abc12345678_chapters.json"
    )
    assert str(cleaned_store.cleaned_path(PLAYLIST, "abc12345678", "v2_content")) == (
        f"GeminiLongContext/{PLAYLIST}/abc12345678_v2_content.json"
    )
    assert str(cleaned_store.cleaned_path(PLAYLIST, "abc12345678", "lecture_context")) == (
        f"GeminiLongContext/{PLAYLIST}/abc12345678_lecture_context.json"
    )


def test_existing_cleaned_returns_only_present_roles(tmp_path):
    seed_corpus(tmp_path)
    found = cleaned_store.existing_cleaned(
        PLAYLIST, "abc12345678", root=tmp_path / "GeminiLongContext"
    )
    assert set(found) == {"chapters", "v2_content", "lecture_context", "content"}
    assert cleaned_store.existing_cleaned(
        PLAYLIST, "ghi01234567", root=tmp_path / "GeminiLongContext"
    ) == {}


def test_iter_raw_videos_skips_support_directories(tmp_path):
    seed_corpus(tmp_path)
    pairs = [
        (playlist_id, video_id)
        for playlist_id, video_id, _ in cleaned_store.iter_raw_videos(tmp_path / "data")
    ]
    assert pairs == [(PLAYLIST, "abc12345678"), (PLAYLIST, "def45678901"), (PLAYLIST, "ghi01234567")]


def test_source_coverage_pairs_raw_with_cleaned_counterparts(tmp_path):
    seed_corpus(tmp_path)
    coverage = cleaned_store.source_coverage(
        raw_root=tmp_path / "data", cleaned_root=tmp_path / "GeminiLongContext"
    )
    assert coverage["counts"] == {
        "chapters": 1,
        "v2_content": 1,
        "lecture_context": 2,
        "content": 1,
    }
    assert coverage["videos_without_cleaned"] == [f"{PLAYLIST}/ghi01234567"]

    abc = next(v for v in coverage["videos"] if v["video_id"] == "abc12345678")
    assert abc["playlist_id"] == PLAYLIST
    assert abc["raw_path"].endswith(f"{PLAYLIST}/abc12345678_raw.json")
    assert set(abc["cleaned"]) == {"chapters", "v2_content", "lecture_context", "content"}

    ghi = next(v for v in coverage["videos"] if v["video_id"] == "ghi01234567")
    assert ghi["cleaned"] == {}


def test_source_coverage_tolerates_missing_roots(tmp_path):
    coverage = cleaned_store.source_coverage(
        raw_root=tmp_path / "data", cleaned_root=tmp_path / "GeminiLongContext"
    )
    assert coverage == {"videos": [], "counts": {
        "chapters": 0, "v2_content": 0, "lecture_context": 0, "content": 0,
    }, "videos_without_cleaned": []}
