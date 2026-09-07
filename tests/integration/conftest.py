"""Shared doubles for the main-pipeline integration tests."""
import pytest


@pytest.fixture(autouse=True)
def _fake_cleaned_source_report(monkeypatch):
    """Keep pipeline tests off the real GeminiLongContext/ tree: main() must
    report cleaned sources without touching the local corpus in tests."""
    monkeypatch.setattr(
        "main.report_cleaned_sources",
        lambda: {"videos": [], "counts": {}, "videos_without_cleaned": []},
    )
