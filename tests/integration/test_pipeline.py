"""
Integration tests for the main pipeline in main.py.
"""
import pytest
import os
import pandas as pd
from unittest.mock import Mock, patch, MagicMock, mock_open
from main import main


class TestMainPipelineIntegration:
    """Integration tests for the main pipeline function."""
    
    @patch('main.get_db_connection')
    @patch('main.conn_sync')
    @patch('main.extract.process_playlists')
    @patch('main.load.insert_videos_to_db')
    @patch('main.extract.download_file_from_r2')
    @patch('main.load.update_downloaded_r2')
    @patch('main.transform.fix_typos')
    @patch('main.os.path.exists')
    @patch('main.os.makedirs')
    @patch('main.os.scandir')
    def test_main_pipeline_complete_success(
        self,
        mock_scandir,
        mock_makedirs,
        mock_exists,
        mock_fix_typos,
        mock_update_downloaded,
        mock_download_r2,
        mock_insert_videos,
        mock_process_playlists,
        mock_conn_sync,
        mock_get_conn
    ):
        """Test complete successful pipeline execution."""
        # Mock database connection and sync
        mock_connection = Mock()
        mock_get_conn.return_value = mock_connection
        
        # Mock unsynced videos query
        mock_connection.execute.return_value.fetchall.return_value = [
            ('video123', 'playlist456'),
            ('video789', 'playlist456')
        ]
        
        # Mock file system operations - files don't exist initially so they get downloaded
        mock_exists.return_value = False
        
        # Mock directory scanning for transcript processing
        mock_playlist_dir = Mock()
        mock_playlist_dir.name = 'playlist456'
        mock_playlist_dir.is_dir.return_value = True
        mock_playlist_dir.path = 'data/playlist456'
        
        mock_raw_file = Mock()
        mock_raw_file.name = 'video123_raw.json'
        
        mock_scandir.side_effect = [
            [mock_playlist_dir],  # First call for playlist directories
            [mock_raw_file]       # Second call for raw files in playlist
        ]
        
        # Mock successful operations
        mock_download_r2.return_value = True
        mock_fix_typos.return_value = True
        
        with patch('builtins.print'):
            main()
        
        # Verify all pipeline steps were called
        mock_conn_sync.assert_called_once()
        mock_process_playlists.assert_called_once_with("new_iugaza1")
        mock_insert_videos.assert_called_once_with("new_iugaza1_video_data.xlsx")
        
        # Verify database query for unsynced videos
        mock_connection.execute.assert_called_with(
            "SELECT video_id, playlist_id FROM sync_github WHERE downloaded_r2 = 0 OR downloaded_r2 IS NULL"
        )
        
        # Verify R2 downloads - should be called for each unsynced video
        expected_download_calls = 2
        assert mock_download_r2.call_count == expected_download_calls
        
        # Verify status updates - should be called for each successful download
        expected_update_calls = 2  # Both downloads succeed
        assert mock_update_downloaded.call_count == expected_update_calls
    
    @patch('main.get_db_connection')
    @patch('main.conn_sync')
    @patch('main.extract.process_playlists')
    @patch('main.load.insert_videos_to_db')
    def test_main_pipeline_database_sync_failure(
        self,
        mock_insert_videos,
        mock_process_playlists,
        mock_conn_sync,
        mock_get_conn
    ):
        """Test pipeline behavior when database sync fails."""
        mock_conn_sync.side_effect = Exception("Database sync failed")
        
        with pytest.raises(Exception, match="Database sync failed"):
            main()
        
        # Subsequent steps should not be called
        mock_process_playlists.assert_not_called()
        mock_insert_videos.assert_not_called()
    
    @patch('main.get_db_connection')
    @patch('main.conn_sync')
    @patch('main.extract.process_playlists')
    @patch('main.load.insert_videos_to_db')
    def test_main_pipeline_playlist_processing_failure(
        self,
        mock_insert_videos,
        mock_process_playlists,
        mock_conn_sync,
        mock_get_conn
    ):
        """Test pipeline behavior when playlist processing fails."""
        mock_process_playlists.side_effect = Exception("Playlist processing failed")
        
        with pytest.raises(Exception, match="Playlist processing failed"):
            main()
        
        # Database sync should have been called
        mock_conn_sync.assert_called_once()
        # Video insertion should not be called
        mock_insert_videos.assert_not_called()
    
    @patch('main.get_db_connection')
    @patch('main.conn_sync')
    @patch('main.extract.process_playlists')
    @patch('main.load.insert_videos_to_db')
    @patch('main.extract.download_file_from_r2')
    @patch('main.load.update_downloaded_r2')
    @patch('main.os.path.exists')
    @patch('main.os.makedirs')
    def test_main_pipeline_partial_r2_download_failures(
        self,
        mock_makedirs,
        mock_exists,
        mock_update_downloaded,
        mock_download_r2,
        mock_insert_videos,
        mock_process_playlists,
        mock_conn_sync,
        mock_get_conn
    ):
        """Test pipeline with some R2 download failures."""
        # Mock database operations
        mock_connection = Mock()
        mock_get_conn.return_value = mock_connection
        mock_connection.execute.return_value.fetchall.return_value = [
            ('video123', 'playlist456'),
            ('video789', 'playlist456')
        ]
        
        # Mock file operations
        mock_exists.return_value = False  # Files don't exist initially
        
        # Mock partial download success
        def download_side_effect(*args):
            video_id = args[0]
            return video_id == 'video123'  # Only first download succeeds
        
        mock_download_r2.side_effect = download_side_effect
        
        with patch('builtins.print'), patch('main.os.scandir', return_value=[]):
            main()
        
        # Verify all downloads were attempted
        assert mock_download_r2.call_count == 2
        
        # Verify only successful download was marked as complete
        mock_update_downloaded.assert_called_once_with('video123', 'playlist456', 1)
    
    @patch('main.get_db_connection')
    @patch('main.conn_sync')
    @patch('main.extract.process_playlists')
    @patch('main.load.insert_videos_to_db')
    @patch('main.os.scandir')
    def test_main_pipeline_no_unsynced_videos(
        self,
        mock_scandir,
        mock_insert_videos,
        mock_process_playlists,
        mock_conn_sync,
        mock_get_conn
    ):
        """Test pipeline when no unsynced videos exist."""
        # Mock database operations
        mock_connection = Mock()
        mock_get_conn.return_value = mock_connection
        mock_connection.execute.return_value.fetchall.return_value = []  # No unsynced videos
        
        # Mock empty data directories
        mock_scandir.return_value = []
        
        with patch('builtins.print'):
            main()
        
        # Early steps should still be called
        mock_conn_sync.assert_called_once()
        mock_process_playlists.assert_called_once()
        mock_insert_videos.assert_called_once()
        
        # Directory scanning should still happen but find nothing
        mock_scandir.assert_called_once_with("data")
    
    @patch('main.get_db_connection')
    @patch('main.conn_sync')
    @patch('main.extract.process_playlists')
    @patch('main.load.insert_videos_to_db')
    @patch('main.extract.download_file_from_r2')
    @patch('main.load.update_downloaded_r2')
    @patch('main.transform.fix_typos')
    @patch('main.os.path.exists')
    @patch('main.os.makedirs')
    @patch('main.os.scandir')
    def test_main_pipeline_transcript_processing(
        self,
        mock_scandir,
        mock_makedirs,
        mock_exists,
        mock_fix_typos,
        mock_update_downloaded,
        mock_download_r2,
        mock_insert_videos,
        mock_process_playlists,
        mock_conn_sync,
        mock_get_conn
    ):
        """Test transcript processing portion of pipeline."""
        # Mock database operations
        mock_connection = Mock()
        mock_get_conn.return_value = mock_connection
        mock_connection.execute.return_value.fetchall.return_value = []  # No downloads needed
        
        # Mock directory structure for transcript processing
        mock_playlist_dir = Mock()
        mock_playlist_dir.name = 'playlist456'
        mock_playlist_dir.is_dir.return_value = True
        mock_playlist_dir.path = 'data/playlist456'
        
        mock_raw_file1 = Mock()
        mock_raw_file1.name = 'video123_raw.json'
        mock_raw_file2 = Mock()
        mock_raw_file2.name = 'video789_raw.json'
        
        mock_scandir.side_effect = [
            [mock_playlist_dir],                    # Playlist directories
            [mock_raw_file1, mock_raw_file2]        # Raw files in playlist
        ]
        
        # Mock file existence checks
        def exists_side_effect(path):
            if 'processed' in path:
                return 'video123' not in path  # video123 needs processing
            if 'final' in path:
                return 'video789' not in path  # video789 needs final processing
            return True
        
        mock_exists.side_effect = exists_side_effect
        mock_fix_typos.return_value = True
        
        with patch('builtins.print'):
            main()
        
        # Verify typo fixing was called for video789 (needs final processing)
        mock_fix_typos.assert_called_once_with(
            'data/processed/playlist456/video789.srt',
            'data/final/playlist456/video789_clarified.srt'
        )

    @patch('main.get_db_connection')
    @patch('main.conn_sync')
    @patch('main.extract.process_playlists')
    @patch('main.load.insert_videos_to_db')
    @patch('main.transform.fix_typos')
    @patch('main.os.path.exists')
    @patch('main.os.makedirs')
    @patch('main.os.scandir')
    def test_main_pipeline_skips_support_directories(
        self,
        mock_scandir,
        mock_makedirs,
        mock_exists,
        mock_fix_typos,
        mock_insert_videos,
        mock_process_playlists,
        mock_conn_sync,
        mock_get_conn
    ):
        """Playlists sit directly under data/; raw/processed/final support dirs are not playlists."""
        mock_connection = Mock()
        mock_get_conn.return_value = mock_connection
        mock_connection.execute.return_value.fetchall.return_value = []

        mock_playlist_dir = Mock()
        mock_playlist_dir.name = 'PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-'
        mock_playlist_dir.is_dir.return_value = True
        mock_playlist_dir.path = 'data/PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-'

        support_dirs = []
        for name in ('raw', 'processed', 'final'):
            entry = Mock()
            entry.name = name
            entry.is_dir.return_value = True
            support_dirs.append(entry)

        mock_scandir.side_effect = [
            [*support_dirs, mock_playlist_dir],  # data/ scan
            [],                                  # files inside the playlist directory
        ]

        with patch('builtins.print'):
            main()

        # Only data/ and the real playlist directory are scanned; support dirs are skipped
        scanned = [call.args[0] for call in mock_scandir.call_args_list]
        assert scanned == ['data', 'data/PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-']
        mock_fix_typos.assert_not_called()

    @patch('main.get_db_connection')
    @patch('main.conn_sync')
    @patch('main.extract.process_playlists')
    @patch('main.load.insert_videos_to_db')
    @patch('main.transform.fix_typos')
    @patch('main.os.path.exists')
    @patch('main.os.makedirs')
    @patch('main.os.scandir')
    def test_main_pipeline_ignores_non_raw_json(
        self,
        mock_scandir,
        mock_makedirs,
        mock_exists,
        mock_fix_typos,
        mock_insert_videos,
        mock_process_playlists,
        mock_conn_sync,
        mock_get_conn
    ):
        """Only <video_id>_raw.json names drive processing; other JSON files are not transcripts."""
        mock_connection = Mock()
        mock_get_conn.return_value = mock_connection
        mock_connection.execute.return_value.fetchall.return_value = []

        mock_playlist_dir = Mock()
        mock_playlist_dir.name = 'playlist456'
        mock_playlist_dir.is_dir.return_value = True
        mock_playlist_dir.path = 'data/playlist456'

        mock_stray_json = Mock()
        mock_stray_json.name = 'video123_v2_content.json'

        mock_scandir.side_effect = [
            [mock_playlist_dir],   # data/ scan
            [mock_stray_json],     # files inside the playlist directory
        ]

        mock_exists.return_value = False

        with patch('builtins.print'):
            main()

        mock_fix_typos.assert_not_called()
    
    @patch('main.get_db_connection')
    @patch('main.conn_sync')
    @patch('main.extract.process_playlists')
    @patch('main.load.insert_videos_to_db')
    @patch('main.os.scandir')
    def test_main_pipeline_directory_scanning_error(
        self,
        mock_scandir,
        mock_insert_videos,
        mock_process_playlists,
        mock_conn_sync,
        mock_get_conn
    ):
        """Test pipeline handling of directory scanning errors."""
        # Mock database operations
        mock_connection = Mock()
        mock_get_conn.return_value = mock_connection
        mock_connection.execute.return_value.fetchall.return_value = []
        
        # Mock directory scanning failure
        mock_scandir.side_effect = FileNotFoundError("Directory not found")
        
        with pytest.raises(FileNotFoundError, match="Directory not found"):
            main()
        
        # Earlier steps should have completed
        mock_conn_sync.assert_called_once()
        mock_process_playlists.assert_called_once()
        mock_insert_videos.assert_called_once()


class TestMainPipelineFileOperations:
    """Test file system operations in the main pipeline."""
    
    @patch('main.get_db_connection')
    @patch('main.conn_sync')
    @patch('main.extract.process_playlists')
    @patch('main.load.insert_videos_to_db')
    @patch('main.extract.download_file_from_r2')
    @patch('main.load.update_downloaded_r2')
    def test_main_pipeline_directory_creation(
        self,
        mock_update_downloaded,
        mock_download_r2,
        mock_insert_videos,
        mock_process_playlists,
        mock_conn_sync,
        mock_get_conn
    ):
        """Test that directories are created when they don't exist."""
        # Mock database operations
        mock_connection = Mock()
        mock_get_conn.return_value = mock_connection
        mock_connection.execute.return_value.fetchall.return_value = [
            ('video123', 'playlist456')
        ]
        
        with patch('main.os.path.exists') as mock_exists, \
             patch('main.os.makedirs') as mock_makedirs, \
             patch('main.os.scandir', return_value=[]), \
             patch('builtins.print'):
            
            mock_exists.return_value = False  # Local file doesn't exist
            mock_download_r2.return_value = True
            
            main()
            
            # Verify directory creation
            mock_makedirs.assert_called_once_with('data/playlist456', exist_ok=True)
    
    @patch('main.get_db_connection')
    @patch('main.conn_sync')
    @patch('main.extract.process_playlists')
    @patch('main.load.insert_videos_to_db')
    @patch('main.extract.download_file_from_r2')
    @patch('main.load.update_downloaded_r2')
    def test_main_pipeline_file_path_construction(
        self,
        mock_update_downloaded,
        mock_download_r2,
        mock_insert_videos,
        mock_process_playlists,
        mock_conn_sync,
        mock_get_conn
    ):
        """Test correct file path construction for downloads."""
        # Mock database operations
        mock_connection = Mock()
        mock_get_conn.return_value = mock_connection
        mock_connection.execute.return_value.fetchall.return_value = [
            ('video123', 'playlist456'),
            ('video789', 'playlist789')
        ]
        
        with patch('main.os.path.exists', return_value=False), \
             patch('main.os.makedirs'), \
             patch('main.os.scandir', return_value=[]), \
             patch('builtins.print'):
            
            mock_download_r2.return_value = True
            
            main()
            
            # Verify correct file paths were constructed
            expected_calls = [
                ('video123', 'youtube-iug-asdj', 'data/playlist456/video123_raw.json'),
                ('video789', 'youtube-iug-asdj', 'data/playlist789/video789_raw.json')
            ]
            
            actual_calls = mock_download_r2.call_args_list
            for expected, actual in zip(expected_calls, actual_calls):
                assert actual[0] == expected


class TestMainPipelineErrorHandling:
    """Test error handling in the main pipeline."""
    
    @patch('main.conn_sync')
    def test_main_pipeline_prints_status_messages(self, mock_conn_sync):
        """Test that pipeline prints appropriate status messages."""
        with patch('main.extract.process_playlists') as mock_process, \
             patch('main.load.insert_videos_to_db') as mock_insert, \
             patch('main.get_db_connection') as mock_get_conn, \
             patch('main.os.scandir', return_value=[]), \
             patch('builtins.print') as mock_print:
            
            mock_connection = Mock()
            mock_get_conn.return_value = mock_connection
            mock_connection.execute.return_value.fetchall.return_value = []
            
            main()
            
            # Verify status messages were printed
            expected_messages = [
                "Starting the IUG Course Transcripts pipeline...",
                "Fetching playlist data...",
                "Inserting video data into the database...",
                "Downloading raw transcripts...",
                "Locating cleaned sources...",
                "Processing transcripts...",
                "Pipeline finished."
            ]
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            for expected in expected_messages:
                assert expected in print_calls


class TestMainPipelineEndToEnd:
    """End-to-end pipeline tests with realistic scenarios."""
    
    def test_main_pipeline_imports(self):
        """Test that all required imports are working."""
        # This test ensures all imports in main.py work correctly
        try:
            import main
            from src.etl import extract, transform, load
            from src.ai import gemini
            from src.database import get_db_connection, conn_sync
            from src.utils import open_file
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
    
    def test_main_function_exists_and_callable(self):
        """Test that main function exists and is callable."""
        from main import main
        assert callable(main)
    
    @patch('main.get_db_connection')
    @patch('main.conn_sync')
    @patch('main.extract.process_playlists')
    @patch('main.load.insert_videos_to_db')
    @patch('main.extract.download_file_from_r2')
    @patch('main.load.update_downloaded_r2')
    @patch('main.transform.fix_typos')
    @patch('main.os.path.exists')
    @patch('main.os.makedirs')
    @patch('main.os.scandir')
    def test_realistic_pipeline_scenario(
        self,
        mock_scandir,
        mock_makedirs,
        mock_exists,
        mock_fix_typos,
        mock_update_downloaded,
        mock_download_r2,
        mock_insert_videos,
        mock_process_playlists,
        mock_conn_sync,
        mock_get_conn
    ):
        """Test a realistic pipeline scenario with multiple videos and playlists."""
        # Setup realistic database response
        mock_connection = Mock()
        mock_get_conn.return_value = mock_connection
        mock_connection.execute.return_value.fetchall.return_value = [
            ('abc123', 'CS101'),
            ('def456', 'CS101'),
            ('ghi789', 'MATH201'),
        ]
        
        # Setup realistic directory structure
        cs_dir = Mock()
        cs_dir.name = 'CS101'
        cs_dir.is_dir.return_value = True
        cs_dir.path = 'data/CS101'
        
        math_dir = Mock()
        math_dir.name = 'MATH201'
        math_dir.is_dir.return_value = True
        math_dir.path = 'data/MATH201'
        
        cs_file1 = Mock()
        cs_file1.name = 'abc123_raw.json'
        cs_file2 = Mock()
        cs_file2.name = 'def456_raw.json'
        
        math_file1 = Mock()
        math_file1.name = 'ghi789_raw.json'
        
        mock_scandir.side_effect = [
            [cs_dir, math_dir],           # Main data directory
            [cs_file1, cs_file2],         # CS101 directory
            [math_file1]                  # MATH201 directory
        ]
        
        # Setup file existence - some files need processing
        def exists_side_effect(path):
            if 'processed' in path:
                return 'abc123' not in path  # abc123 needs processing
            if 'final' in path:
                return 'def456' in path      # def456 already processed
            return False  # Raw files don't exist initially
        
        mock_exists.side_effect = exists_side_effect
        
        # Setup successful operations
        mock_download_r2.return_value = True
        mock_fix_typos.return_value = True
        
        with patch('builtins.print'):
            main()
        
        # Verify comprehensive pipeline execution
        mock_conn_sync.assert_called_once()
        mock_process_playlists.assert_called_once_with("new_iugaza1")
        mock_insert_videos.assert_called_once_with("new_iugaza1_video_data.xlsx")
        
        # Verify all videos were processed for download
        assert mock_download_r2.call_count == 3
        assert mock_update_downloaded.call_count == 3
        
        # Verify transcript processing
        assert mock_fix_typos.call_count == 2  # abc123 and ghi789 need processing