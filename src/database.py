import libsql_experimental as libsql
from .config import TURSO_DATABASE_URL, TURSO_AUTH_TOKEN, DB_PATH

def get_db_connection():
    return libsql.connect(DB_PATH, sync_url=TURSO_DATABASE_URL, auth_token=TURSO_AUTH_TOKEN)

def conn_sync():
    conn = get_db_connection()
    conn.execute("SELECT 1")
    conn.commit()
    conn.sync()

def get_playlist_data(playlist_id):
    conn = get_db_connection()
    query = "SELECT * FROM playlists where source_id='" + playlist_id + "';"
    cursor = conn.cursor()
    cursor.execute(query)
    desc = cursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    return data
