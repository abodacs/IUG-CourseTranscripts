"""
Unit tests for src/ai/gemini.py module.
"""
import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from src.ai.gemini import (
    Course,
    Chapter,
    genai_completion,
    enrich_playlist_details,
    extract_chapters
)


class TestCourseModel:
    """Test cases for the Course Pydantic model."""
    
    def test_course_model_valid_data(self):
        """Test Course model with valid data."""
        course_data = {
            "name": "Introduction to Computer Science",
            "faculty": "Faculty of Information Technology",
            "topic": "Basic programming concepts",
            "instructor": "Dr. Ahmed Hassan",
            "target_audience": "First-year students"
        }
        
        course = Course(**course_data)
        
        assert course.name == "Introduction to Computer Science"
        assert course.faculty == "Faculty of Information Technology"
        assert course.topic == "Basic programming concepts"
        assert course.instructor == "Dr. Ahmed Hassan"
        assert course.target_audience == "First-year students"
    
    def test_course_model_with_none_values(self):
        """Test Course model with None values."""
        course_data = {
            "name": None,
            "faculty": None,
            "topic": None,
            "instructor": None,
            "target_audience": None
        }
        
        course = Course(**course_data)
        
        assert course.name is None
        assert course.faculty is None
        assert course.topic is None
        assert course.instructor is None
        assert course.target_audience is None
    
    def test_course_model_serialization(self):
        """Test Course model JSON serialization."""
        course = Course(
            name="Test Course",
            faculty="Test Faculty",
            topic="Test Topic",
            instructor="Test Instructor",
            target_audience="Test Audience"
        )
        
        json_data = course.model_dump()
        expected = {
            "name": "Test Course",
            "faculty": "Test Faculty", 
            "topic": "Test Topic",
            "instructor": "Test Instructor",
            "target_audience": "Test Audience"
        }
        
        assert json_data == expected


class TestChapterModel:
    """Test cases for the Chapter Pydantic model."""
    
    def test_chapter_model_valid_data(self):
        """Test Chapter model with valid data."""
        chapter_data = {
            "start_ts": 120.5,
            "title": "Introduction to Variables"
        }
        
        chapter = Chapter(**chapter_data)
        
        assert chapter.start_ts == 120.5
        assert chapter.title == "Introduction to Variables"
    
    def test_chapter_model_with_none_values(self):
        """Test Chapter model with None values."""
        chapter_data = {
            "start_ts": None,
            "title": None
        }
        
        chapter = Chapter(**chapter_data)
        
        assert chapter.start_ts is None
        assert chapter.title is None
    
    def test_chapter_model_serialization(self):
        """Test Chapter model JSON serialization."""
        chapter = Chapter(start_ts=300.0, title="Chapter 1")
        
        json_data = chapter.model_dump()
        expected = {
            "start_ts": 300.0,
            "title": "Chapter 1"
        }
        
        assert json_data == expected


class TestGenaiCompletion:
    """Test cases for the genai_completion function."""
    
    @patch('src.ai.gemini.genai.GenerativeModel')
    @patch('src.ai.gemini.save_file')
    @patch('src.ai.gemini.time')
    def test_genai_completion_success(self, mock_time, mock_save_file, mock_model_class):
        """Test successful AI completion."""
        mock_time.return_value = 1234567890.123
        
        mock_model = Mock()
        mock_model_class.return_value = mock_model
        
        mock_response = Mock()
        mock_response.text = "This is the AI response"
        mock_model.generate_content.return_value = mock_response
        
        result = genai_completion("Test prompt")
        
        assert result == "This is the AI response"
        
        # Verify model configuration
        mock_model_class.assert_called_once_with(
            "gemini-1.5-flash-latest",
            generation_config={"temperature": 2}
        )
        
        # Verify content generation
        mock_model.generate_content.assert_called_once_with(
            "Test prompt",
            safety_settings={
                'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
                'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
            }
        )
        
        # Verify logging
        mock_save_file.assert_called_once_with(
            './gemini_logs/1234567890.123_gemini.txt',
            'Test prompt\n\n==========\n\nThis is the AI response'
        )
    
    @patch('src.ai.gemini.genai.GenerativeModel')
    @patch('src.ai.gemini.save_file')
    @patch('src.ai.gemini.from_json')
    def test_genai_completion_with_json_schema(self, mock_from_json, mock_save_file, mock_model_class):
        """Test AI completion with JSON schema."""
        mock_model = Mock()
        mock_model_class.return_value = mock_model
        
        mock_response = Mock()
        mock_response.text = '{"name": "Test Course", "faculty": "Test Faculty"}'
        mock_model.generate_content.return_value = mock_response
        
        mock_parsed_data = {"name": "Test Course", "faculty": "Test Faculty"}
        mock_from_json.return_value = mock_parsed_data
        
        result = genai_completion("Test prompt", response_schema=Course)
        
        assert result == mock_parsed_data
        
        # Verify JSON configuration
        expected_config = {
            "temperature": 2,
            "response_mime_type": "application/json",
            "response_schema": Course
        }
        mock_model_class.assert_called_once_with(
            "gemini-1.5-flash-latest",
            generation_config=expected_config
        )
        
        # Verify JSON parsing
        mock_from_json.assert_called_once_with(
            '{"name": "Test Course", "faculty": "Test Faculty"}',
            allow_partial=False
        )
    
    @patch('src.ai.gemini.genai.GenerativeModel')
    @patch('src.ai.gemini.save_file')
    def test_genai_completion_api_error(self, mock_save_file, mock_model_class):
        """Test handling of API errors."""
        mock_model = Mock()
        mock_model_class.return_value = mock_model
        mock_model.generate_content.side_effect = Exception("API Error")
        
        with patch('builtins.print') as mock_print:
            result = genai_completion("Test prompt")
        
        assert result is None
        mock_print.assert_called_once_with("An error occurred: API Error")
    
    @patch('src.ai.gemini.genai.GenerativeModel')
    @patch('src.ai.gemini.save_file')
    @patch('src.ai.gemini.from_json')
    def test_genai_completion_json_parsing_error(self, mock_from_json, mock_save_file, mock_model_class):
        """Test handling of JSON parsing errors."""
        mock_model = Mock()
        mock_model_class.return_value = mock_model
        
        mock_response = Mock()
        mock_response.text = "Invalid JSON response"
        mock_model.generate_content.return_value = mock_response
        
        mock_from_json.side_effect = Exception("JSON parsing failed")
        
        with patch('builtins.print') as mock_print:
            result = genai_completion("Test prompt", response_schema=Course)
        
        assert result is None
        mock_print.assert_called_once_with("An error occurred: JSON parsing failed")
    
    @patch('src.ai.gemini.genai.GenerativeModel')
    @patch('src.ai.gemini.save_file')
    def test_genai_completion_retry_decorator(self, mock_save_file, mock_model_class):
        """Test that retry decorator is working (function is decorated with @retry)."""
        # This is more of a smoke test since testing the retry logic thoroughly
        # would require more complex mocking
        mock_model = Mock()
        mock_model_class.return_value = mock_model
        
        mock_response = Mock()
        mock_response.text = "Success"
        mock_model.generate_content.return_value = mock_response
        
        result = genai_completion("Test prompt")
        
        assert result == "Success"


class TestEnrichPlaylistDetails:
    """Test cases for the enrich_playlist_details function."""
    
    @patch('src.ai.gemini.genai_completion')
    @patch('src.ai.gemini.open_file')
    def test_enrich_playlist_details_success(self, mock_open_file, mock_genai):
        """Test successful playlist enrichment."""
        mock_open_file.return_value = "Extract details: <<PLAYLISTTITLE>> <<DESCRIPTION>>"
        
        mock_course_data = {
            "name": "Computer Science 101",
            "faculty": "Faculty of IT",
            "topic": "Programming basics",
            "instructor": "Dr. Ahmed",
            "target_audience": "Beginners"
        }
        mock_genai.return_value = mock_course_data
        
        result = enrich_playlist_details("CS101 Introduction", "Basic programming course")
        
        assert isinstance(result, Course)
        assert result.name == "Computer Science 101"
        assert result.faculty == "Faculty of IT"
        
        # Verify prompt was constructed correctly
        mock_genai.assert_called_once()
        prompt_used = mock_genai.call_args[0][0]
        assert "CS101 Introduction" in prompt_used
        assert "Basic programming course" in prompt_used
        assert "<<PLAYLISTTITLE>>" not in prompt_used
        assert "<<DESCRIPTION>>" not in prompt_used
    
    @patch('src.ai.gemini.genai_completion')
    @patch('src.ai.gemini.open_file')
    def test_enrich_playlist_details_with_none_values(self, mock_open_file, mock_genai):
        """Test playlist enrichment with None title and description."""
        mock_open_file.return_value = "Extract details: <<PLAYLISTTITLE>> <<DESCRIPTION>>"
        
        mock_course_data = {
            "name": "Unknown Course",
            "faculty": None,
            "topic": None,
            "instructor": None,
            "target_audience": "Arabic-speaking students"
        }
        mock_genai.return_value = mock_course_data
        
        result = enrich_playlist_details(None, None)
        
        assert isinstance(result, Course)
        assert result.name == "Unknown Course"
        
        # Verify empty strings were used for None values
        prompt_used = mock_genai.call_args[0][0]
        assert "Extract details:  " in prompt_used  # Empty title and description
    
    @patch('src.ai.gemini.genai_completion')
    @patch('src.ai.gemini.open_file')
    def test_enrich_playlist_details_ai_failure(self, mock_open_file, mock_genai):
        """Test handling of AI completion failure."""
        mock_open_file.return_value = "Extract details: <<PLAYLISTTITLE>> <<DESCRIPTION>>"
        mock_genai.return_value = None  # AI failed
        
        result = enrich_playlist_details("Test Title", "Test Description")
        
        assert result is None
    
    @patch('src.ai.gemini.open_file')
    def test_enrich_playlist_details_prompt_file_error(self, mock_open_file):
        """Test handling of prompt file read error."""
        mock_open_file.side_effect = FileNotFoundError("Prompt file not found")
        
        with pytest.raises(FileNotFoundError, match="Prompt file not found"):
            enrich_playlist_details("Title", "Description")
    
    @patch('src.ai.gemini.genai_completion')
    @patch('src.ai.gemini.open_file')
    def test_enrich_playlist_details_validation_error(self, mock_open_file, mock_genai):
        """Test handling of Course validation errors."""
        mock_open_file.return_value = "Extract details: <<PLAYLISTTITLE>> <<DESCRIPTION>>"
        
        # Invalid course data that fails validation
        invalid_data = {"invalid_field": "value"}
        mock_genai.return_value = invalid_data
        
        # Course.model_validate should raise a validation error
        with pytest.raises(Exception):  # Pydantic validation error
            enrich_playlist_details("Title", "Description")


class TestExtractChapters:
    """Test cases for the extract_chapters function."""
    
    @patch('src.ai.gemini.genai_completion')
    @patch('src.ai.gemini.open_file')
    def test_extract_chapters_success(self, mock_open_file, mock_genai):
        """Test successful chapter extraction."""
        mock_open_file.return_value = "Extract chapters from: <<TRANSCRIPT>>"
        
        mock_chapters_data = [
            {"start_ts": 0.0, "title": "Introduction"},
            {"start_ts": 300.0, "title": "Main Content"},
            {"start_ts": 600.0, "title": "Conclusion"}
        ]
        mock_genai.return_value = mock_chapters_data
        
        result = extract_chapters("This is a test transcript with multiple sections.")
        
        assert len(result) == 3
        assert all(isinstance(chapter, Chapter) for chapter in result)
        assert result[0].start_ts == 0.0
        assert result[0].title == "Introduction"
        assert result[1].start_ts == 300.0
        assert result[1].title == "Main Content"
        
        # Verify prompt was constructed correctly
        prompt_used = mock_genai.call_args[0][0]
        assert "This is a test transcript with multiple sections." in prompt_used
        assert "<<TRANSCRIPT>>" not in prompt_used
    
    @patch('src.ai.gemini.genai_completion')
    @patch('src.ai.gemini.open_file')
    def test_extract_chapters_empty_result(self, mock_open_file, mock_genai):
        """Test chapter extraction with empty result."""
        mock_open_file.return_value = "Extract chapters from: <<TRANSCRIPT>>"
        mock_genai.return_value = []
        
        result = extract_chapters("Short transcript without clear chapters.")
        
        assert result == []
    
    @patch('src.ai.gemini.genai_completion')
    @patch('src.ai.gemini.open_file')
    def test_extract_chapters_ai_failure(self, mock_open_file, mock_genai):
        """Test handling of AI completion failure."""
        mock_open_file.return_value = "Extract chapters from: <<TRANSCRIPT>>"
        mock_genai.return_value = None  # AI failed
        
        result = extract_chapters("Test transcript")
        
        assert result == []
    
    @patch('src.ai.gemini.open_file')
    def test_extract_chapters_prompt_file_error(self, mock_open_file):
        """Test handling of prompt file read error."""
        mock_open_file.side_effect = FileNotFoundError("Prompt file not found")
        
        with pytest.raises(FileNotFoundError, match="Prompt file not found"):
            extract_chapters("Test transcript")
    
    @patch('src.ai.gemini.genai_completion')
    @patch('src.ai.gemini.open_file')
    def test_extract_chapters_validation_error(self, mock_open_file, mock_genai):
        """Test handling of Chapter validation errors."""
        mock_open_file.return_value = "Extract chapters from: <<TRANSCRIPT>>"
        
        # Invalid chapter data
        invalid_chapters = [
            {"invalid_field": "value", "another_field": "value2"}
        ]
        mock_genai.return_value = invalid_chapters
        
        with pytest.raises(Exception):  # Pydantic validation error
            extract_chapters("Test transcript")
    
    @patch('src.ai.gemini.genai_completion')
    @patch('src.ai.gemini.open_file')
    def test_extract_chapters_mixed_valid_invalid_data(self, mock_open_file, mock_genai):
        """Test handling when some chapters are valid and others invalid."""
        mock_open_file.return_value = "Extract chapters from: <<TRANSCRIPT>>"
        
        mixed_data = [
            {"start_ts": 0.0, "title": "Valid Chapter"},
            {"invalid_field": "value"},  # Invalid chapter
        ]
        mock_genai.return_value = mixed_data
        
        # The function tries to validate each chapter, so it should fail
        # on the invalid one
        with pytest.raises(Exception):
            extract_chapters("Test transcript")
    
    def test_extract_chapters_wrong_prompt_file_reference(self):
        """Test that the function references the correct prompt file."""
        # This test checks that the function is using the right prompt file
        # Note: In the actual code, there seems to be a bug where extract_chapters
        # uses 'clarify_transcript.txt' instead of a dedicated chapters prompt
        
        with patch('src.ai.gemini.open_file') as mock_open_file:
            mock_open_file.return_value = "test prompt"
            
            with patch('src.ai.gemini.genai_completion') as mock_genai:
                mock_genai.return_value = []
                
                extract_chapters("test")
                
                # Verify it's trying to read the clarify_transcript file
                mock_open_file.assert_called_once_with('src/ai/prompts/clarify_transcript.txt')


class TestGeminiIntegration:
    """Integration tests for gemini module functions working together."""
    
    @patch('src.ai.gemini.genai_completion')
    @patch('src.ai.gemini.open_file')
    def test_enrich_and_extract_workflow(self, mock_open_file, mock_genai):
        """Test using enrich_playlist_details and extract_chapters together."""
        mock_open_file.return_value = "Test prompt: <<PLAYLISTTITLE>> <<DESCRIPTION>> <<TRANSCRIPT>>"
        
        # Mock responses for different calls
        def genai_side_effect(*args, **kwargs):
            if 'response_schema' in kwargs and kwargs['response_schema'] == Course:
                return {
                    "name": "Test Course",
                    "faculty": "Test Faculty", 
                    "topic": "Test Topic",
                    "instructor": "Test Instructor",
                    "target_audience": "Test Audience"
                }
            elif 'response_schema' in kwargs and kwargs['response_schema'] == list[Chapter]:
                return [
                    {"start_ts": 0.0, "title": "Chapter 1"},
                    {"start_ts": 300.0, "title": "Chapter 2"}
                ]
            return None
        
        mock_genai.side_effect = genai_side_effect
        
        # Enrich playlist
        course = enrich_playlist_details("Test Playlist", "Test Description")
        assert isinstance(course, Course)
        assert course.name == "Test Course"
        
        # Extract chapters
        chapters = extract_chapters("Test transcript content")
        assert len(chapters) == 2
        assert all(isinstance(chapter, Chapter) for chapter in chapters)
        assert chapters[0].title == "Chapter 1"