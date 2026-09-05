"""
Unit tests for src/utils.py module.
"""
import pytest
import os
from src.utils import open_file, save_file, batched


class TestOpenFile:
    """Test cases for the open_file function."""
    
    def test_open_existing_file(self, temp_directory):
        """Test opening an existing file."""
        test_content = "Hello, World!\nThis is a test file."
        test_file = os.path.join(temp_directory, "test.txt")
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        result = open_file(test_file)
        assert result == test_content
    
    def test_open_file_with_unicode(self, temp_directory):
        """Test opening a file with Unicode characters."""
        test_content = "مرحبا بالعالم\nこんにちは世界\n你好世界"
        test_file = os.path.join(temp_directory, "unicode_test.txt")
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        result = open_file(test_file)
        assert result == test_content
    
    def test_open_empty_file(self, temp_directory):
        """Test opening an empty file."""
        test_file = os.path.join(temp_directory, "empty.txt")
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("")
        
        result = open_file(test_file)
        assert result == ""
    
    def test_open_nonexistent_file(self):
        """Test opening a non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            open_file("nonexistent_file.txt")


class TestSaveFile:
    """Test cases for the save_file function."""
    
    def test_save_new_file(self, temp_directory):
        """Test saving content to a new file."""
        test_content = "This is test content."
        test_file = os.path.join(temp_directory, "new_file.txt")
        
        save_file(test_file, test_content)
        
        # Verify file was created and content is correct
        assert os.path.exists(test_file)
        with open(test_file, 'r', encoding='utf-8') as f:
            assert f.read() == test_content
    
    def test_save_overwrite_existing_file(self, temp_directory):
        """Test overwriting an existing file."""
        test_file = os.path.join(temp_directory, "existing_file.txt")
        original_content = "Original content"
        new_content = "New content"
        
        # Create file with original content
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(original_content)
        
        # Overwrite with new content
        save_file(test_file, new_content)
        
        # Verify content was overwritten
        with open(test_file, 'r', encoding='utf-8') as f:
            assert f.read() == new_content
    
    def test_save_file_with_unicode(self, temp_directory):
        """Test saving a file with Unicode characters."""
        test_content = "مرحبا بالعالم\nこんにちは世界\n你好世界"
        test_file = os.path.join(temp_directory, "unicode_save.txt")
        
        save_file(test_file, test_content)
        
        # Verify Unicode content was saved correctly
        with open(test_file, 'r', encoding='utf-8') as f:
            assert f.read() == test_content
    
    def test_save_empty_content(self, temp_directory):
        """Test saving empty content to a file."""
        test_file = os.path.join(temp_directory, "empty_save.txt")
        
        save_file(test_file, "")
        
        # Verify empty file was created
        assert os.path.exists(test_file)
        with open(test_file, 'r', encoding='utf-8') as f:
            assert f.read() == ""
    
    def test_save_to_nonexistent_directory(self):
        """Test saving to a non-existent directory raises an error."""
        with pytest.raises(FileNotFoundError):
            save_file("/nonexistent/directory/file.txt", "content")


class TestBatched:
    """Test cases for the batched function."""
    
    def test_batch_list_evenly_divisible(self):
        """Test batching a list that's evenly divisible by batch size."""
        data = ['A', 'B', 'C', 'D', 'E', 'F']
        result = list(batched(data, 3))
        expected = [('A', 'B', 'C'), ('D', 'E', 'F')]
        assert result == expected
    
    def test_batch_list_not_evenly_divisible(self):
        """Test batching a list that's not evenly divisible by batch size."""
        data = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        result = list(batched(data, 3))
        expected = [('A', 'B', 'C'), ('D', 'E', 'F'), ('G',)]
        assert result == expected
    
    def test_batch_empty_iterable(self):
        """Test batching an empty iterable."""
        result = list(batched([], 3))
        assert result == []
    
    def test_batch_single_item(self):
        """Test batching a single item."""
        data = ['A']
        result = list(batched(data, 3))
        expected = [('A',)]
        assert result == expected
    
    def test_batch_size_one(self):
        """Test batching with size 1."""
        data = ['A', 'B', 'C']
        result = list(batched(data, 1))
        expected = [('A',), ('B',), ('C',)]
        assert result == expected
    
    def test_batch_size_larger_than_data(self):
        """Test batching with size larger than data."""
        data = ['A', 'B']
        result = list(batched(data, 5))
        expected = [('A', 'B')]
        assert result == expected
    
    def test_batch_string_iterable(self):
        """Test batching a string iterable."""
        data = "ABCDEFG"
        result = list(batched(data, 3))
        expected = [('A', 'B', 'C'), ('D', 'E', 'F'), ('G',)]
        assert result == expected
    
    def test_batch_range_iterable(self):
        """Test batching a range iterable."""
        data = range(10)
        result = list(batched(data, 4))
        expected = [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9)]
        assert result == expected
    
    def test_batch_invalid_size_zero(self):
        """Test that batch size 0 raises ValueError."""
        with pytest.raises(ValueError, match="n must be at least one"):
            list(batched([1, 2, 3], 0))
    
    def test_batch_invalid_size_negative(self):
        """Test that negative batch size raises ValueError."""
        with pytest.raises(ValueError, match="n must be at least one"):
            list(batched([1, 2, 3], -1))
    
    def test_batch_generator_input(self):
        """Test batching with a generator input."""
        def data_generator():
            for i in range(7):
                yield f"item_{i}"
        
        result = list(batched(data_generator(), 3))
        expected = [
            ('item_0', 'item_1', 'item_2'),
            ('item_3', 'item_4', 'item_5'),
            ('item_6',)
        ]
        assert result == expected


class TestIntegration:
    """Integration tests for utils functions working together."""
    
    def test_save_and_open_file_roundtrip(self, temp_directory):
        """Test saving a file and then opening it."""
        test_content = "This is a roundtrip test.\nLine 2\nLine 3"
        test_file = os.path.join(temp_directory, "roundtrip.txt")
        
        # Save the file
        save_file(test_file, test_content)
        
        # Open the file
        result = open_file(test_file)
        
        # Verify content matches
        assert result == test_content
    
    def test_batched_with_file_content(self, temp_directory):
        """Test using batched function with file content."""
        lines = ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"]
        content = "\n".join(lines)
        test_file = os.path.join(temp_directory, "batch_test.txt")
        
        # Save content
        save_file(test_file, content)
        
        # Read and batch the lines
        file_content = open_file(test_file)
        file_lines = file_content.split("\n")
        batched_lines = list(batched(file_lines, 2))
        
        expected = [('Line 1', 'Line 2'), ('Line 3', 'Line 4'), ('Line 5',)]
        assert batched_lines == expected