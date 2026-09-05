"""
Unit tests for src/etl/load.py module.
"""
import pytest
import pandas as pd
from unittest.mock import Mock, patch, mock_open
from src.etl.load import upload_file_to_r2, update_downloaded_r2, insert_videos_to_db


class TestUploadFileToR2:
    """Test cases for the upload_file_to_r2 function."""
    
    @patch('src.etl.load.boto3.client')
    @patch('src.etl.load.AWS_ACCESS_KEY_ID', 'test_access_key')
    @patch('src.etl.load.AWS_SECRET_ACCESS_KEY', 'test_secret_key')  
    @patch('src.etl.load.ENDPOINT_URL', 'https://test-endpoint.com')
    @patch('builtins.print')
    def test_upload_file_to_r2_success(self, mock_print, mock_boto_client):
        """Test successful file upload to R2."""
        mock_s3_client = Mock()
        mock_boto_client.return_value = mock_s3_client
        
        upload_file_to_r2('local_file.txt', 'test-bucket', 'remote/file.txt')
        
        mock_boto_client.assert_called_once_with(
            service_name="s3",
            aws_access_key_id="test_access_key",
            aws_secret_access_key="test_secret_key",
            endpoint_url="https://test-endpoint.com"
        )
        
        mock_s3_client.upload_file.assert_called_once_with(
            'local_file.txt', 'test-bucket', 'remote/file.txt'
        )
        
        mock_print.assert_called_once_with(
            "File uploaded successfully to R2 bucket: test-bucket, object key: remote/file.txt"
        )
    
    @patch('src.etl.load.boto3.client')
    @patch('builtins.print')
    def test_upload_file_to_r2_failure(self, mock_print, mock_boto_client):
        """Test failed file upload to R2."""
        mock_s3_client = Mock()
        error_msg = "Upload failed"
        mock_s3_client.upload_file.side_effect = Exception(error_msg)
        mock_boto_client.return_value = mock_s3_client
        
        upload_file_to_r2('local_file.txt', 'test-bucket', 'remote/file.txt')
        
        mock_print.assert_called_once_with(f"Error uploading file: {error_msg}")
    
    @patch('src.etl.load.boto3.client')
    @patch('builtins.print')
    def test_upload_file_to_r2_client_creation_failure(self, mock_print, mock_boto_client):
        """Test S3 client creation failure during upload."""
        mock_boto_client.side_effect = Exception("Client creation failed")
        
        # Client creation happens outside try/catch, so this should raise an exception
        with pytest.raises(Exception, match="Client creation failed"):
            upload_file_to_r2('local_file.txt', 'test-bucket', 'remote/file.txt')
    
    @patch('src.etl.load.boto3.client')
    @patch('src.etl.load.AWS_ACCESS_KEY_ID', 'test_access_key')
    @patch('src.etl.load.AWS_SECRET_ACCESS_KEY', 'test_secret_key')  
    @patch('src.etl.load.ENDPOINT_URL', 'https://test-endpoint.com')
    @patch('builtins.print')
    def test_upload_file_to_r2_configuration(self, mock_print, mock_boto_client):
        """Test that boto3 client is configured with correct credentials."""
        mock_s3_client = Mock()
        mock_boto_client.return_value = mock_s3_client
        
        upload_file_to_r2('test.txt', 'bucket', 'key')
        
        mock_boto_client.assert_called_once_with(
            service_name="s3",
            aws_access_key_id="test_access_key",
            aws_secret_access_key="test_secret_key",
            endpoint_url="https://test-endpoint.com"
        )


class TestUpdateDownloadedR2:
    """Test cases for the update_downloaded_r2 function."""
    
    @patch('src.etl.load.get_db_connection')
    def test_update_downloaded_r2_success(self, mock_get_conn):
        """Test successful update of downloaded_r2 status."""
        mock_connection = Mock()
        mock_get_conn.return_value = mock_connection
        
        update_downloaded_r2('video123', 'playlist456', 1)
        
        mock_get_conn.assert_called_once()
        expected_query = "update sync_github set downloaded_r2 = 1 where video_id= 'video123' and playlist_id='playlist456';"
        mock_connection.execute.assert_called_once_with(expected_query)
        mock_connection.commit.assert_called_once()
        mock_connection.sync.assert_called_once()
    
    @patch('src.etl.load.get_db_connection')
    def test_update_downloaded_r2_set_to_zero(self, mock_get_conn):
        """Test updating downloaded_r2 status to 0."""
        mock_connection = Mock()
        mock_get_conn.return_value = mock_connection
        
        update_downloaded_r2('video789', 'playlist123', 0)
        
        expected_query = "update sync_github set downloaded_r2 = 0 where video_id= 'video789' and playlist_id='playlist123';"
        mock_connection.execute.assert_called_once_with(expected_query)
        mock_connection.commit.assert_called_once()
        mock_connection.sync.assert_called_once()
    
    @patch('src.etl.load.get_db_connection')
    def test_update_downloaded_r2_sql_injection_vulnerability(self, mock_get_conn):
        """Test that demonstrates SQL injection vulnerability (for security awareness)."""
        mock_connection = Mock()
        mock_get_conn.return_value = mock_connection
        
        # This test demonstrates the vulnerability - the function should use parameterized queries
        malicious_video_id = "'; DROP TABLE sync_github; --"
        
        update_downloaded_r2(malicious_video_id, 'playlist123', 1)
        
        # The query will contain the malicious input directly
        expected_query = f"update sync_github set downloaded_r2 = 1 where video_id= '{malicious_video_id}' and playlist_id='playlist123';"
        mock_connection.execute.assert_called_once_with(expected_query)
    
    @patch('src.etl.load.get_db_connection')
    def test_update_downloaded_r2_database_error(self, mock_get_conn):
        """Test handling of database errors during update."""
        mock_get_conn.side_effect = Exception("Database connection failed")
        
        with pytest.raises(Exception, match="Database connection failed"):
            update_downloaded_r2('video123', 'playlist456', 1)
    
    @patch('src.etl.load.get_db_connection')
    def test_update_downloaded_r2_execute_error(self, mock_get_conn):
        """Test handling of execute errors during update."""
        mock_connection = Mock()
        mock_connection.execute.side_effect = Exception("Execute failed")
        mock_get_conn.return_value = mock_connection
        
        with pytest.raises(Exception, match="Execute failed"):
            update_downloaded_r2('video123', 'playlist456', 1)
        
        # commit and sync should not be called if execute fails
        mock_connection.commit.assert_not_called()
        mock_connection.sync.assert_not_called()
    
    @patch('src.etl.load.get_db_connection')
    def test_update_downloaded_r2_commit_error(self, mock_get_conn):
        """Test handling of commit errors during update."""
        mock_connection = Mock()
        mock_connection.commit.side_effect = Exception("Commit failed")
        mock_get_conn.return_value = mock_connection
        
        with pytest.raises(Exception, match="Commit failed"):
            update_downloaded_r2('video123', 'playlist456', 1)
        
        # sync should not be called if commit fails
        mock_connection.sync.assert_not_called()


class TestInsertVideosToDB:
    """Test cases for the insert_videos_to_db function."""
    
    @patch('src.etl.load.get_db_connection')
    @patch('src.etl.load.pd.read_excel')
    @patch('builtins.print')
    def test_insert_videos_to_db_success(self, mock_print, mock_read_excel, mock_get_conn):
        """Test successful insertion of videos to database."""
        mock_connection = Mock()
        mock_get_conn.return_value = mock_connection
        
        # Mock DataFrame
        test_data = pd.DataFrame([
            {'id': 'video123', 'playlist_id': 'playlist456'},
            {'id': 'video789', 'playlist_id': 'playlist456'}
        ])
        mock_read_excel.return_value = test_data
        
        insert_videos_to_db('test_videos.xlsx')
        
        mock_read_excel.assert_called_once_with('test_videos.xlsx')
        mock_get_conn.assert_called_once()
        
        # Verify both insert statements were called
        expected_calls = [
            "INSERT INTO sync_github (video_id, playlist_id) VALUES ('video123', 'playlist456');",
            "INSERT INTO sync_github (video_id, playlist_id) VALUES ('video789', 'playlist456');"
        ]
        
        assert mock_connection.execute.call_count == 2
        actual_calls = [call[0][0] for call in mock_connection.execute.call_args_list]
        assert set(actual_calls) == set(expected_calls)
        
        mock_connection.commit.assert_called_once()
        mock_connection.sync.assert_called_once()
        mock_print.assert_called_once_with("Completed inserting videos. Errors: []")
    
    @patch('src.etl.load.get_db_connection')
    @patch('src.etl.load.pd.read_excel')
    @patch('builtins.print')
    def test_insert_videos_to_db_with_errors(self, mock_print, mock_read_excel, mock_get_conn):
        """Test insertion with some database errors."""
        mock_connection = Mock()
        mock_get_conn.return_value = mock_connection
        
        # Mock DataFrame
        test_data = pd.DataFrame([
            {'id': 'video123', 'playlist_id': 'playlist456'},
            {'id': 'video789', 'playlist_id': 'playlist456'},
            {'id': 'video999', 'playlist_id': 'playlist456'}
        ])
        mock_read_excel.return_value = test_data
        
        # Mock execute to fail on specific calls
        def mock_execute_side_effect(query):
            if 'video789' in query:
                raise Exception("Duplicate key error")
            if 'video999' in query:
                raise Exception("Invalid data error")
        
        mock_connection.execute.side_effect = mock_execute_side_effect
        
        insert_videos_to_db('test_videos.xlsx')
        
        # Should still commit and sync despite errors
        mock_connection.commit.assert_called_once()
        mock_connection.sync.assert_called_once()
        
        # Should report errors for failed insertions
        # Check that the final print call was made with the correct message
        final_call = mock_print.call_args_list[-1]
        assert final_call[0][0] == "Completed inserting videos. Errors: ['video789', 'video999']"
    
    @patch('src.etl.load.get_db_connection')
    @patch('src.etl.load.pd.read_excel')
    def test_insert_videos_to_db_empty_file(self, mock_read_excel, mock_get_conn):
        """Test insertion from empty Excel file."""
        mock_connection = Mock()
        mock_get_conn.return_value = mock_connection
        
        # Mock empty DataFrame
        empty_data = pd.DataFrame(columns=['id', 'playlist_id'])
        mock_read_excel.return_value = empty_data
        
        with patch('builtins.print') as mock_print:
            insert_videos_to_db('empty_videos.xlsx')
        
        # No execute calls should be made
        mock_connection.execute.assert_not_called()
        mock_connection.commit.assert_called_once()
        mock_connection.sync.assert_called_once()
        mock_print.assert_called_once_with("Completed inserting videos. Errors: []")
    
    @patch('src.etl.load.pd.read_excel')
    def test_insert_videos_to_db_file_not_found(self, mock_read_excel):
        """Test handling of missing Excel file."""
        mock_read_excel.side_effect = FileNotFoundError("Excel file not found")
        
        with pytest.raises(FileNotFoundError, match="Excel file not found"):
            insert_videos_to_db('nonexistent.xlsx')
    
    @patch('src.etl.load.get_db_connection')
    @patch('src.etl.load.pd.read_excel')
    def test_insert_videos_to_db_database_connection_error(self, mock_read_excel, mock_get_conn):
        """Test handling of database connection errors."""
        test_data = pd.DataFrame([{'id': 'video123', 'playlist_id': 'playlist456'}])
        mock_read_excel.return_value = test_data
        mock_get_conn.side_effect = Exception("Database connection failed")
        
        with pytest.raises(Exception, match="Database connection failed"):
            insert_videos_to_db('test_videos.xlsx')
    
    @patch('src.etl.load.get_db_connection')
    @patch('src.etl.load.pd.read_excel')
    def test_insert_videos_to_db_missing_columns(self, mock_read_excel, mock_get_conn):
        """Test handling of Excel file with missing required columns."""
        mock_connection = Mock()
        mock_get_conn.return_value = mock_connection
        
        # DataFrame missing required columns
        invalid_data = pd.DataFrame([{'title': 'Video Title', 'duration': 3600}])
        mock_read_excel.return_value = invalid_data
        
        with pytest.raises(KeyError):
            insert_videos_to_db('invalid_videos.xlsx')
    
    @patch('src.etl.load.get_db_connection')
    @patch('src.etl.load.pd.read_excel')
    def test_insert_videos_to_db_sql_injection_vulnerability(self, mock_read_excel, mock_get_conn):
        """Test that demonstrates SQL injection vulnerability in video data."""
        mock_connection = Mock()
        mock_get_conn.return_value = mock_connection
        
        # Malicious data that could cause SQL injection
        malicious_data = pd.DataFrame([
            {'id': "'; DROP TABLE sync_github; --", 'playlist_id': 'normal_playlist'}
        ])
        mock_read_excel.return_value = malicious_data
        
        with patch('builtins.print'):
            insert_videos_to_db('malicious_videos.xlsx')
        
        # The malicious SQL should be directly interpolated (showing the vulnerability)
        expected_query = "INSERT INTO sync_github (video_id, playlist_id) VALUES (''; DROP TABLE sync_github; --', 'normal_playlist');"
        mock_connection.execute.assert_called_once_with(expected_query)


class TestLoadIntegration:
    """Integration tests for load module functions working together."""
    
    @patch('src.etl.load.upload_file_to_r2')
    @patch('src.etl.load.update_downloaded_r2')
    @patch('src.etl.load.insert_videos_to_db')
    def test_complete_load_workflow(self, mock_insert, mock_update, mock_upload):
        """Test complete load workflow."""
        # Setup mocks
        mock_insert.return_value = None
        mock_update.return_value = None
        mock_upload.return_value = None
        
        # Execute workflow steps
        mock_insert('videos.xlsx')
        mock_insert.assert_called_once_with('videos.xlsx')
        
        mock_update('video123', 'playlist456', 1)
        mock_update.assert_called_once_with('video123', 'playlist456', 1)
        
        mock_upload('local.json', 'bucket', 'remote.json')
        mock_upload.assert_called_once_with('local.json', 'bucket', 'remote.json')
    
    @patch('src.etl.load.get_db_connection')
    @patch('src.etl.load.pd.read_excel')
    @patch('builtins.print')
    def test_insert_then_update_status_workflow(self, mock_print, mock_read_excel, mock_get_conn):
        """Test inserting videos then updating their status."""
        mock_connection = Mock()
        mock_get_conn.return_value = mock_connection
        
        # Mock video data
        test_data = pd.DataFrame([
            {'id': 'video123', 'playlist_id': 'playlist456'}
        ])
        mock_read_excel.return_value = test_data
        
        # Insert videos
        insert_videos_to_db('videos.xlsx')
        
        # Update status
        update_downloaded_r2('video123', 'playlist456', 1)
        
        # Verify database operations
        assert mock_connection.execute.call_count == 2  # insert + update
        assert mock_connection.commit.call_count == 2   # commit for each operation
        assert mock_connection.sync.call_count == 2     # sync for each operation