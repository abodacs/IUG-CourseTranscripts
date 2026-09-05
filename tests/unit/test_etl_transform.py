"""
Unit tests for src/etl/transform.py module.
"""
import pytest
import pysrt
import os
from unittest.mock import Mock, patch, mock_open
from src.etl.transform import (
    get_transcripts,
    format_timestamp,
    write_srt,
    fix_typos
)


class TestGetTranscripts:
    """Test cases for the get_transcripts function."""
    
    @patch('src.etl.transform.pysrt.open')
    def test_get_transcripts_success(self, mock_pysrt_open):
        """Test successful transcript loading."""
        mock_sub1 = Mock()
        mock_sub1.start = pysrt.SubRipTime(0, 0, 5, 0)
        mock_sub1.end = pysrt.SubRipTime(0, 0, 10, 0)
        mock_sub1.text = "Welcome to the course"
        
        mock_sub2 = Mock()
        mock_sub2.start = pysrt.SubRipTime(0, 0, 10, 0)
        mock_sub2.end = pysrt.SubRipTime(0, 0, 15, 0)
        mock_sub2.text = "Today we will learn"
        
        mock_subs = [mock_sub1, mock_sub2]
        mock_pysrt_open.return_value = mock_subs
        
        result = get_transcripts('test.srt')
        
        mock_pysrt_open.assert_called_once_with('test.srt')
        assert result == mock_subs
        assert len(result) == 2
    
    @patch('src.etl.transform.pysrt.open')
    def test_get_transcripts_empty_file(self, mock_pysrt_open):
        """Test transcript loading from empty file."""
        mock_pysrt_open.return_value = []
        
        result = get_transcripts('empty.srt')
        
        mock_pysrt_open.assert_called_once_with('empty.srt')
        assert result == []
    
    @patch('src.etl.transform.pysrt.open')
    def test_get_transcripts_file_not_found(self, mock_pysrt_open):
        """Test handling of missing SRT file."""
        mock_pysrt_open.side_effect = FileNotFoundError("SRT file not found")
        
        with pytest.raises(FileNotFoundError, match="SRT file not found"):
            get_transcripts('nonexistent.srt')
    
    @patch('src.etl.transform.pysrt.open')
    def test_get_transcripts_invalid_format(self, mock_pysrt_open):
        """Test handling of invalid SRT format."""
        mock_pysrt_open.side_effect = Exception("Invalid SRT format")
        
        with pytest.raises(Exception, match="Invalid SRT format"):
            get_transcripts('invalid.srt')


class TestFormatTimestamp:
    """Test cases for the format_timestamp function."""
    
    def test_format_timestamp_basic(self):
        """Test basic timestamp formatting."""
        result = format_timestamp(65.5)
        assert result == "01:05.500"
    
    def test_format_timestamp_with_hours(self):
        """Test timestamp formatting with hours."""
        result = format_timestamp(3665.123)  # 1 hour, 1 minute, 5.123 seconds
        assert result == "01:01:05.123"
    
    def test_format_timestamp_zero(self):
        """Test formatting zero timestamp."""
        result = format_timestamp(0)
        assert result == "00:00.000"
    
    def test_format_timestamp_milliseconds_precision(self):
        """Test timestamp with millisecond precision."""
        result = format_timestamp(123.456789)
        assert result == "02:03.457"  # Should round milliseconds
    
    def test_format_timestamp_always_include_hours(self):
        """Test formatting with always_include_hours=True."""
        result = format_timestamp(65.5, always_include_hours=True)
        assert result == "00:01:05.500"
    
    def test_format_timestamp_custom_decimal_marker(self):
        """Test formatting with custom decimal marker."""
        result = format_timestamp(65.5, decimal_marker=",")
        assert result == "01:05,500"
    
    def test_format_timestamp_large_value(self):
        """Test formatting very large timestamp."""
        result = format_timestamp(86461.999)  # 24+ hours
        assert result == "24:01:01.999"
    
    def test_format_timestamp_none_value(self):
        """Test formatting None timestamp."""
        result = format_timestamp(None)
        assert result is None
    
    def test_format_timestamp_negative_value(self):
        """Test formatting negative timestamp raises assertion error."""
        with pytest.raises(AssertionError, match="non-negative timestamp expected"):
            format_timestamp(-10.0)
    
    def test_format_timestamp_edge_cases(self):
        """Test various edge cases."""
        # Exactly 1 hour
        assert format_timestamp(3600.0) == "01:00:00.000"
        
        # Just under 1 hour
        assert format_timestamp(3599.999) == "59:59.999"
        
        # Very small value
        assert format_timestamp(0.001) == "00:00.001"
        
        # Exactly 1 minute
        assert format_timestamp(60.0) == "01:00.000"


class TestWriteSrt:
    """Test cases for the write_srt function."""
    
    def test_write_srt_with_dict_segments(self):
        """Test writing SRT with dictionary segments."""
        segments = [
            {"start": 0.0, "end": 5.0, "text": "Welcome to the course"},
            {"start": 5.0, "end": 10.0, "text": "Today we will learn"},
        ]
        
        mock_file = Mock()
        write_srt(mock_file, segments)
        
        expected_calls = [
            mock_file.write.call_args_list[0][0][0],  # "1\n"
            mock_file.write.call_args_list[1][0][0],  # "00:00:00,000 --> 00:00:05,000\n"
            mock_file.write.call_args_list[2][0][0],  # "Welcome to the course"
            mock_file.write.call_args_list[3][0][0],  # "\n\n"
        ]
        
        assert "1\n" in expected_calls
        assert "00:00:00,000 --> 00:00:05,000\n" in expected_calls
        assert mock_file.write.call_count == 8  # 4 calls per segment × 2 segments
    
    def test_write_srt_with_object_segments(self):
        """Test writing SRT with object segments."""
        mock_segment1 = Mock()
        mock_segment1.start = 0.0
        mock_segment1.end = 5.0
        mock_segment1.text = "First subtitle"
        
        mock_segment2 = Mock()
        mock_segment2.start = 5.0
        mock_segment2.end = 10.0
        mock_segment2.text = "Second subtitle"
        
        segments = [mock_segment1, mock_segment2]
        
        mock_file = Mock()
        write_srt(mock_file, segments)
        
        # Should have 8 write calls (4 per segment)
        assert mock_file.write.call_count == 8
        
        # Check that sequence numbers are correct
        call_args = [call[0][0] for call in mock_file.write.call_args_list]
        assert "1\n" in call_args
        assert "2\n" in call_args
    
    def test_write_srt_arrow_replacement(self):
        """Test that arrows in text are replaced."""
        segments = [
            {"start": 0.0, "end": 5.0, "text": "This --> should be replaced"}
        ]
        
        mock_file = Mock()
        write_srt(mock_file, segments)
        
        # Find the text write call
        call_args = [call[0][0] for call in mock_file.write.call_args_list]
        text_written = None
        for arg in call_args:
            if "should be replaced" in arg:
                text_written = arg
                break
        
        assert text_written is not None
        assert "-->" not in text_written
        assert "->" in text_written
    
    def test_write_srt_text_stripping(self):
        """Test that text is stripped of whitespace."""
        segments = [
            {"start": 0.0, "end": 5.0, "text": "  Text with whitespace  \n"}
        ]
        
        mock_file = Mock()
        write_srt(mock_file, segments)
        
        # Check that text was stripped
        call_args = [call[0][0] for call in mock_file.write.call_args_list]
        for arg in call_args:
            if "Text with whitespace" in arg:
                assert arg == "Text with whitespace"
                break
        else:
            pytest.fail("Expected text not found in write calls")
    
    def test_write_srt_empty_segments(self):
        """Test writing SRT with empty segments list."""
        segments = []
        
        mock_file = Mock()
        write_srt(mock_file, segments)
        
        mock_file.write.assert_not_called()
    
    def test_write_srt_timestamp_format(self):
        """Test SRT timestamp format (with comma decimal marker)."""
        segments = [
            {"start": 65.123, "end": 130.456, "text": "Test text"}
        ]
        
        mock_file = Mock()
        write_srt(mock_file, segments)
        
        # Find the timestamp write call
        call_args = [call[0][0] for call in mock_file.write.call_args_list]
        timestamp_line = None
        for arg in call_args:
            if "-->" in arg and "," in arg:
                timestamp_line = arg
                break
        
        assert timestamp_line is not None
        assert "00:01:05,123 --> 00:02:10,456\n" == timestamp_line


class TestFixTypos:
    """Test cases for the fix_typos function."""
    
    @patch('src.etl.transform.genai_completion')
    @patch('src.etl.transform.open_file')
    @patch('src.etl.transform.save_file')
    @patch('src.etl.transform.batched')
    def test_fix_typos_success(self, mock_batched, mock_save_file, mock_open_file, mock_genai):
        """Test successful typo fixing."""
        # Mock file reading
        transcript_content = "1\n00:00:00,000 --> 00:00:05,000\nHelo world\n\n2\n00:00:05,000 --> 00:00:10,000\nThis is a tets"
        prompt_content = "Fix typos in: <<TRANSCRIPT>>"
        
        def mock_open_side_effect(filepath):
            if 'transcript' in filepath:
                return transcript_content
            elif 'prompts/clarify_transcript.txt' in filepath:
                return prompt_content
            return ""
        
        mock_open_file.side_effect = mock_open_side_effect
        
        # Mock batching
        chunks = [
            ("1\n00:00:00,000 --> 00:00:05,000\nHelo world",),
            ("2\n00:00:05,000 --> 00:00:10,000\nThis is a tets",)
        ]
        mock_batched.return_value = chunks
        
        # Mock AI responses
        ai_responses = [
            "1\n00:00:00,000 --> 00:00:05,000\nHello world",
            "2\n00:00:05,000 --> 00:00:10,000\nThis is a test"
        ]
        mock_genai.side_effect = ai_responses
        
        result = fix_typos('input.srt', 'output.srt')
        
        assert result is True
        mock_open_file.assert_called()
        mock_genai.assert_called()
        mock_save_file.assert_called_once()
        
        # Verify the corrected content was saved
        save_call = mock_save_file.call_args[0]
        saved_content = save_call[1]
        assert "Hello world" in saved_content
        assert "This is a test" in saved_content
    
    @patch('src.etl.transform.genai_completion')
    @patch('src.etl.transform.open_file')
    @patch('src.etl.transform.save_file')
    @patch('src.etl.transform.batched')
    def test_fix_typos_with_code_blocks(self, mock_batched, mock_save_file, mock_open_file, mock_genai):
        """Test fixing typos with code block markers removal."""
        mock_open_file.side_effect = lambda x: "test content" if 'transcript' in x else "Fix: <<TRANSCRIPT>>"
        mock_batched.return_value = [("chunk1",)]
        
        # AI response with code blocks
        mock_genai.return_value = "```\nCorrected text\n```"
        
        result = fix_typos('input.srt', 'output.srt')
        
        assert result is True
        mock_save_file.assert_called_once()
        
        # Verify code blocks were removed
        saved_content = mock_save_file.call_args[0][1]
        assert "```" not in saved_content
        assert "Corrected text" in saved_content
    
    @patch('src.etl.transform.genai_completion')
    @patch('src.etl.transform.open_file')
    @patch('src.etl.transform.save_file')
    @patch('src.etl.transform.batched')
    def test_fix_typos_ai_failure(self, mock_batched, mock_save_file, mock_open_file, mock_genai):
        """Test handling of AI completion failures."""
        mock_open_file.side_effect = lambda x: "test content" if 'transcript' in x else "Fix: <<TRANSCRIPT>>"
        mock_batched.return_value = [("chunk1",)]
        
        # AI returns None (failure)
        mock_genai.return_value = None
        
        result = fix_typos('input.srt', 'output.srt')
        
        assert result is False
        mock_save_file.assert_not_called()
    
    @patch('src.etl.transform.genai_completion')
    @patch('src.etl.transform.open_file')
    @patch('src.etl.transform.save_file')
    @patch('src.etl.transform.batched')
    def test_fix_typos_partial_ai_success(self, mock_batched, mock_save_file, mock_open_file, mock_genai):
        """Test handling when some AI calls succeed and others fail."""
        mock_open_file.side_effect = lambda x: "test content" if 'transcript' in x else "Fix: <<TRANSCRIPT>>"
        mock_batched.return_value = [("chunk1",), ("chunk2",)]
        
        # First AI call succeeds, second fails
        mock_genai.side_effect = ["Corrected chunk 1", None]
        
        result = fix_typos('input.srt', 'output.srt')
        
        assert result is True
        mock_save_file.assert_called_once()
        
        # Only successful chunks should be saved
        saved_content = mock_save_file.call_args[0][1]
        assert "Corrected chunk 1" in saved_content
    
    @patch('src.etl.transform.open_file')
    def test_fix_typos_file_read_error(self, mock_open_file):
        """Test handling of file read errors."""
        mock_open_file.side_effect = FileNotFoundError("File not found")
        
        with pytest.raises(FileNotFoundError, match="File not found"):
            fix_typos('nonexistent.srt', 'output.srt')
    
    @patch('src.etl.transform.genai_completion')
    @patch('src.etl.transform.open_file')
    @patch('src.etl.transform.save_file')
    @patch('src.etl.transform.batched')
    def test_fix_typos_chunk_size_usage(self, mock_batched, mock_save_file, mock_open_file, mock_genai):
        """Test that CHUNK_SIZE is used correctly."""
        from src.config import CHUNK_SIZE
        
        mock_open_file.side_effect = lambda x: "test\n\ncontent" if 'transcript' in x else "Fix: <<TRANSCRIPT>>"
        mock_genai.return_value = "fixed"
        
        fix_typos('input.srt', 'output.srt')
        
        # Verify batched was called with the correct chunk size
        mock_batched.assert_called_once()
        call_args = mock_batched.call_args
        assert call_args[0][1] == CHUNK_SIZE  # Second argument should be CHUNK_SIZE
    
    @patch('src.etl.transform.genai_completion')
    @patch('src.etl.transform.open_file')
    @patch('src.etl.transform.save_file')
    @patch('src.etl.transform.batched')
    def test_fix_typos_prompt_replacement(self, mock_batched, mock_save_file, mock_open_file, mock_genai):
        """Test that prompt template is correctly replaced."""
        transcript_content = "test transcript content"
        prompt_template = "Please fix: <<TRANSCRIPT>>"
        
        def mock_open_side_effect(filepath):
            if 'input.srt' in filepath:
                return transcript_content
            elif 'prompts/clarify_transcript.txt' in filepath:
                return prompt_template
            return ""
        
        mock_open_file.side_effect = mock_open_side_effect
        mock_batched.return_value = [(transcript_content,)]
        mock_genai.return_value = "fixed content"
        
        fix_typos('input.srt', 'output.srt')
        
        # Verify genai was called with prompt containing the transcript  
        mock_genai.assert_called_once()
        prompt_used = mock_genai.call_args[0][0]
        assert "Please fix: test transcript content" == prompt_used
        assert "<<TRANSCRIPT>>" not in prompt_used


class TestTransformIntegration:
    """Integration tests for transform module functions working together."""
    
    def test_format_timestamp_in_write_srt(self):
        """Test that format_timestamp is used correctly in write_srt."""
        segments = [{"start": 65.123, "end": 130.456, "text": "Test"}]
        
        mock_file = Mock()
        write_srt(mock_file, segments)
        
        # Find timestamp call and verify format
        call_args = [call[0][0] for call in mock_file.write.call_args_list]
        timestamp_call = None
        for arg in call_args:
            if "01:05,123" in arg and "02:10,456" in arg:
                timestamp_call = arg
                break
        
        assert timestamp_call is not None
    
    @patch('src.etl.transform.pysrt.open')
    def test_get_transcripts_with_write_srt(self, mock_pysrt_open):
        """Test using get_transcripts output with write_srt."""
        # Mock pysrt subtitle objects
        mock_sub = Mock()
        mock_sub.start = 0.0
        mock_sub.end = 5.0
        mock_sub.text = "Test subtitle"
        
        mock_pysrt_open.return_value = [mock_sub]
        
        # Get transcripts
        transcripts = get_transcripts('test.srt')
        
        # Write them using write_srt
        mock_file = Mock()
        write_srt(mock_file, transcripts)
        
        # Verify it worked
        assert mock_file.write.call_count == 4  # 4 calls per subtitle