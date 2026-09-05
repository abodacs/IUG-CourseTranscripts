"""
Unit tests for src/database.py module.
"""
import pytest
from unittest.mock import Mock, patch
from src.database import get_db_connection, conn_sync, get_playlist_data


class TestGetDbConnection:
    """Test cases for the get_db_connection function."""
    
    @patch('src.database.libsql.connect')
    @patch('src.database.TURSO_DATABASE_URL', 'file:test.db')
    @patch('src.database.TURSO_AUTH_TOKEN', 'test_token')
    def test_get_db_connection_success(self, mock_connect):
        """Test successful database connection."""
        mock_connection = Mock()
        mock_connect.return_value = mock_connection
        
        result = get_db_connection()
        
        mock_connect.assert_called_once_with(
            "youtube-iug.db",
            sync_url="file:test.db",
            auth_token="test_token"
        )
        assert result == mock_connection
    
    @patch('src.database.libsql.connect')
    @patch('src.database.TURSO_DATABASE_URL', 'custom_url')
    @patch('src.database.TURSO_AUTH_TOKEN', 'custom_token')
    def test_get_db_connection_with_custom_config(self, mock_connect):
        """Test database connection with custom configuration."""
        mock_connection = Mock()
        mock_connect.return_value = mock_connection
        
        result = get_db_connection()
        
        mock_connect.assert_called_once_with(
            "youtube-iug.db",
            sync_url="custom_url",
            auth_token="custom_token"
        )
        assert result == mock_connection
    
    @patch('src.database.libsql.connect')
    def test_get_db_connection_failure(self, mock_connect):
        """Test database connection failure."""
        mock_connect.side_effect = Exception("Connection failed")
        
        with pytest.raises(Exception, match="Connection failed"):
            get_db_connection()


class TestConnSync:
    """Test cases for the conn_sync function."""
    
    @patch('src.database.get_db_connection')
    def test_conn_sync_success(self, mock_get_conn):
        """Test successful connection synchronization."""
        mock_connection = Mock()
        mock_get_conn.return_value = mock_connection
        
        conn_sync()
        
        mock_get_conn.assert_called_once()
        mock_connection.execute.assert_called_once_with("SELECT 1")
        mock_connection.commit.assert_called_once()
        mock_connection.sync.assert_called_once()
    
    @patch('src.database.get_db_connection')
    def test_conn_sync_execute_failure(self, mock_get_conn):
        """Test connection sync with execute failure."""
        mock_connection = Mock()
        mock_connection.execute.side_effect = Exception("Execute failed")
        mock_get_conn.return_value = mock_connection
        
        with pytest.raises(Exception, match="Execute failed"):
            conn_sync()
        
        mock_get_conn.assert_called_once()
        mock_connection.execute.assert_called_once_with("SELECT 1")
        # commit and sync should not be called if execute fails
        mock_connection.commit.assert_not_called()
        mock_connection.sync.assert_not_called()
    
    @patch('src.database.get_db_connection')
    def test_conn_sync_commit_failure(self, mock_get_conn):
        """Test connection sync with commit failure."""
        mock_connection = Mock()
        mock_connection.commit.side_effect = Exception("Commit failed")
        mock_get_conn.return_value = mock_connection
        
        with pytest.raises(Exception, match="Commit failed"):
            conn_sync()
        
        mock_get_conn.assert_called_once()
        mock_connection.execute.assert_called_once_with("SELECT 1")
        mock_connection.commit.assert_called_once()
        # sync should not be called if commit fails
        mock_connection.sync.assert_not_called()
    
    @patch('src.database.get_db_connection')
    def test_conn_sync_sync_failure(self, mock_get_conn):
        """Test connection sync with sync failure."""
        mock_connection = Mock()
        mock_connection.sync.side_effect = Exception("Sync failed")
        mock_get_conn.return_value = mock_connection
        
        with pytest.raises(Exception, match="Sync failed"):
            conn_sync()
        
        mock_get_conn.assert_called_once()
        mock_connection.execute.assert_called_once_with("SELECT 1")
        mock_connection.commit.assert_called_once()
        mock_connection.sync.assert_called_once()


class TestGetPlaylistData:
    """Test cases for the get_playlist_data function."""
    
    @patch('src.database.get_db_connection')
    def test_get_playlist_data_success(self, mock_get_conn):
        """Test successful playlist data retrieval."""
        mock_connection = Mock()
        mock_cursor = Mock()
        
        # Mock the cursor and its methods
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.description = [('id',), ('source_id',), ('title',), ('description',)]
        mock_cursor.fetchall.return_value = [
            (1, 'playlist123', 'Test Playlist', 'Test description'),
            (2, 'playlist456', 'Another Playlist', 'Another description')
        ]
        
        mock_get_conn.return_value = mock_connection
        
        result = get_playlist_data('playlist123')
        
        mock_get_conn.assert_called_once()
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM playlists where source_id='playlist123';"
        )
        mock_cursor.fetchall.assert_called_once()
        
        expected = [
            {'id': 1, 'source_id': 'playlist123', 'title': 'Test Playlist', 'description': 'Test description'},
            {'id': 2, 'source_id': 'playlist456', 'title': 'Another Playlist', 'description': 'Another description'}
        ]
        assert result == expected
    
    @patch('src.database.get_db_connection')
    def test_get_playlist_data_empty_result(self, mock_get_conn):
        """Test playlist data retrieval with empty result."""
        mock_connection = Mock()
        mock_cursor = Mock()
        
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.description = [('id',), ('source_id',), ('title',)]
        mock_cursor.fetchall.return_value = []
        
        mock_get_conn.return_value = mock_connection
        
        result = get_playlist_data('nonexistent_playlist')
        
        mock_get_conn.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM playlists where source_id='nonexistent_playlist';"
        )
        assert result == []
    
    @patch('src.database.get_db_connection')
    def test_get_playlist_data_with_special_characters(self, mock_get_conn):
        """Test playlist data retrieval with special characters in playlist_id."""
        mock_connection = Mock()
        mock_cursor = Mock()
        
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.description = [('id',), ('source_id',)]
        mock_cursor.fetchall.return_value = [(1, "playlist'with'quotes")]
        
        mock_get_conn.return_value = mock_connection
        
        # Note: This test demonstrates the SQL injection vulnerability
        # The function should use parameterized queries instead
        result = get_playlist_data("playlist'with'quotes")
        
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM playlists where source_id='playlist'with'quotes';"
        )
        assert result == [{'id': 1, 'source_id': "playlist'with'quotes"}]
    
    @patch('src.database.get_db_connection')
    def test_get_playlist_data_execute_failure(self, mock_get_conn):
        """Test playlist data retrieval with execute failure."""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = Exception("Database error")
        
        mock_connection.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_connection
        
        with pytest.raises(Exception, match="Database error"):
            get_playlist_data('playlist123')
    
    @patch('src.database.get_db_connection')
    def test_get_playlist_data_fetchall_failure(self, mock_get_conn):
        """Test playlist data retrieval with fetchall failure."""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.description = [('id',)]
        mock_cursor.fetchall.side_effect = Exception("Fetch error")
        
        mock_connection.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_connection
        
        with pytest.raises(Exception, match="Fetch error"):
            get_playlist_data('playlist123')
    
    @patch('src.database.get_db_connection')
    def test_get_playlist_data_connection_failure(self, mock_get_conn):
        """Test playlist data retrieval with connection failure."""
        mock_get_conn.side_effect = Exception("Connection failed")
        
        with pytest.raises(Exception, match="Connection failed"):
            get_playlist_data('playlist123')
    
    def test_get_playlist_data_none_playlist_id(self):
        """Test playlist data retrieval with None playlist_id."""
        # This demonstrates that the function has a bug - it should handle None properly
        with patch('src.database.get_db_connection') as mock_get_conn:
            mock_connection = Mock()
            mock_cursor = Mock()
            mock_connection.cursor.return_value = mock_cursor
            mock_cursor.description = [('id',)]
            mock_cursor.fetchall.return_value = []
            mock_get_conn.return_value = mock_connection
            
            # This should raise TypeError because None + string fails
            with pytest.raises(TypeError):
                get_playlist_data(None)
    
    def test_get_playlist_data_empty_string_playlist_id(self):
        """Test playlist data retrieval with empty string playlist_id."""
        with patch('src.database.get_db_connection') as mock_get_conn:
            mock_connection = Mock()
            mock_cursor = Mock()
            mock_connection.cursor.return_value = mock_cursor
            mock_cursor.description = [('id',)]
            mock_cursor.fetchall.return_value = []
            mock_get_conn.return_value = mock_connection
            
            result = get_playlist_data('')
            
            mock_cursor.execute.assert_called_once_with(
                "SELECT * FROM playlists where source_id='';"
            )
            assert result == []


class TestDatabaseIntegration:
    """Integration tests for database functions working together."""
    
    @patch('src.database.get_db_connection')
    def test_conn_sync_before_get_playlist_data(self, mock_get_conn):
        """Test using conn_sync before get_playlist_data."""
        mock_connection = Mock()
        mock_cursor = Mock()
        
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.description = [('id',), ('title',)]
        mock_cursor.fetchall.return_value = [(1, 'Test Playlist')]
        
        mock_get_conn.return_value = mock_connection
        
        # First sync the connection
        conn_sync()
        
        # Then get playlist data
        result = get_playlist_data('test123')
        
        # Verify conn_sync operations
        assert mock_get_conn.call_count == 2  # Called twice
        # conn_sync calls execute once, get_playlist_data calls execute once via cursor
        assert mock_connection.execute.call_count == 1  # Only conn_sync calls connection.execute
        # get_playlist_data calls cursor.execute, not connection.execute
        mock_cursor.execute.assert_called_once()
        mock_connection.commit.assert_called_once()
        mock_connection.sync.assert_called_once()
        
        # Verify get_playlist_data result
        assert result == [{'id': 1, 'title': 'Test Playlist'}]