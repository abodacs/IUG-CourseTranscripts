"""
Pytest configuration and shared fixtures for IUG Course Transcripts tests.
"""
import pytest
import os
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
import pandas as pd
from pytest_mock import MockerFixture


@pytest.fixture(autouse=True)
def mock_environment_variables(monkeypatch):
    """Mock environment variables for all tests."""
    test_env_vars = {
        "TURSO_DATABASE_URL": "file:test.db",
        "TURSO_AUTH_TOKEN": "test_token",
        "bucket_name": "test-bucket",
        "aws_access_key_id": "test_access_key",
        "aws_secret_access_key": "test_secret_key",
        "endpoint_url": "https://test-endpoint.com",
        "GEMINI_API_KEY": "test_gemini_key",
        "OPENAI_API_KEY": "test_openai_key",
    }
    for key, value in test_env_vars.items():
        monkeypatch.setenv(key, value)
    
    # Import and patch the config module
    try:
        import src.config
        # Only patch if the module is already loaded
        if hasattr(src.config, 'TURSO_DATABASE_URL'):
            monkeypatch.setattr(src.config, 'TURSO_DATABASE_URL', "file:test.db")
            monkeypatch.setattr(src.config, 'TURSO_AUTH_TOKEN', "test_token")
            monkeypatch.setattr(src.config, 'BUCKET_NAME', "test-bucket")
            monkeypatch.setattr(src.config, 'AWS_ACCESS_KEY_ID', "test_access_key")
            monkeypatch.setattr(src.config, 'AWS_SECRET_ACCESS_KEY', "test_secret_key")
            monkeypatch.setattr(src.config, 'ENDPOINT_URL', "https://test-endpoint.com")
            monkeypatch.setattr(src.config, 'GEMINI_API_KEY', "test_gemini_key")
            monkeypatch.setattr(src.config, 'OPENAI_API_KEY', "test_openai_key")
    except ImportError:
        pass  # Config module not loaded yet


@pytest.fixture
def temp_directory():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def mock_database_connection():
    """Mock database connection for testing."""
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.execute.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []
    mock_cursor.description = [("id",), ("name",)]
    return mock_conn


@pytest.fixture
def sample_video_data():
    """Sample video data for testing."""
    return [
        {
            "id": "video123",
            "title": "Test Video 1",
            "playlist_id": "playlist456",
            "duration": 3600,
        },
        {
            "id": "video789",
            "title": "Test Video 2",
            "playlist_id": "playlist456",
            "duration": 1800,
        }
    ]


@pytest.fixture
def sample_playlist_data():
    """Sample playlist data for testing."""
    return [
        {
            "source_id": "playlist456",
            "title": "Test Playlist",
            "description": "A test playlist for unit testing",
            "process_status": "FINISHED_2",
        }
    ]


@pytest.fixture
def sample_transcript_json():
    """Sample transcript data in JSON format."""
    return {
        "segments": [
            {"start": 0.0, "end": 5.0, "text": "Welcome to the course"},
            {"start": 5.0, "end": 10.0, "text": "Today we will learn about testing"},
            {"start": 10.0, "end": 15.0, "text": "Let's get started"},
        ]
    }


@pytest.fixture
def sample_srt_content():
    """Sample SRT content for testing."""
    return """1
00:00:00,000 --> 00:00:05,000
Welcome to the course

2
00:00:05,000 --> 00:00:10,000
Today we will learn about testing

3
00:00:10,000 --> 00:00:15,000
Let's get started

"""


@pytest.fixture
def mock_yt_dlp_data():
    """Mock yt-dlp extraction data."""
    return {
        "playlist_info": {
            "id": "playlist456",
            "title": "Test Playlist",
            "description": "Test playlist description",
            "entries": []
        },
        "video_entries": [
            {
                "id": "video123",
                "title": "Test Video 1",
                "duration": 3600,
            },
            {
                "id": "video789", 
                "title": "Test Video 2",
                "duration": 1800,
            }
        ]
    }


@pytest.fixture
def mock_s3_client():
    """Mock S3 client for testing."""
    mock_client = Mock()
    mock_client.download_file.return_value = True
    mock_client.upload_file.return_value = True
    return mock_client


@pytest.fixture
def sample_excel_file(temp_directory):
    """Create a sample Excel file for testing."""
    df = pd.DataFrame([
        {"id": "video123", "title": "Test Video 1", "playlist_id": "playlist456"},
        {"id": "video789", "title": "Test Video 2", "playlist_id": "playlist456"}
    ])
    excel_path = os.path.join(temp_directory, "test_videos.xlsx")
    df.to_excel(excel_path, index=False)
    return excel_path


@pytest.fixture
def sample_raw_transcript_file(temp_directory, sample_transcript_json):
    """Create a sample raw transcript JSON file."""
    json_path = os.path.join(temp_directory, "test_transcript_raw.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(sample_transcript_json, f, ensure_ascii=False, indent=2)
    return json_path


@pytest.fixture
def sample_srt_file(temp_directory, sample_srt_content):
    """Create a sample SRT file."""
    srt_path = os.path.join(temp_directory, "test_transcript.srt")
    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write(sample_srt_content)
    return srt_path


@pytest.fixture
def sample_prompt_file(temp_directory):
    """Create a sample prompt file."""
    prompt_content = "Please fix the following transcript: <<TRANSCRIPT>>"
    prompt_path = os.path.join(temp_directory, "test_prompt.txt")
    with open(prompt_path, 'w', encoding='utf-8') as f:
        f.write(prompt_content)
    return prompt_path


@pytest.fixture
def mock_gemini_response():
    """Mock Gemini API response."""
    mock_response = Mock()
    mock_response.text = "This is a corrected transcript with proper formatting."
    return mock_response


@pytest.fixture
def mock_gemini_model():
    """Mock Gemini model for testing."""
    mock_model = Mock()
    mock_model.generate_content.return_value = Mock()
    mock_model.generate_content.return_value.text = "Mocked AI response"
    return mock_model


@pytest.fixture
def mock_course_data():
    """Mock course data for testing."""
    return {
        "name": "Introduction to Computer Science",
        "faculty": "Faculty of Information Technology",
        "topic": "Basic programming and algorithms",
        "instructor": "Dr. Ahmed Hassan, Professor of Computer Science",
        "target_audience": "First-year computer science students"
    }


@pytest.fixture
def mock_chapter_data():
    """Mock chapter data for testing."""
    return [
        {"start_ts": 0.0, "title": "Course Introduction"},
        {"start_ts": 300.0, "title": "Programming Basics"},
        {"start_ts": 900.0, "title": "Control Structures"},
    ]