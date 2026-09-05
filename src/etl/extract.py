import yt_dlp
import pandas as pd
import boto3
from pathlib import Path
from ..database import get_db_connection
from ..config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    ENDPOINT_URL,
)

def get_all_playlists_data():
    conn = get_db_connection()
    query = "SELECT * FROM playlists where process_status = 'FINISHED_2';"
    cursor = conn.cursor()
    cursor.execute(query)
    desc = cursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    return data

def get_playlist_data(playlist_url):
    ydl_opts = {
        'format': 'best',
        'ignoreerrors': True,
        'quiet': True,
        'extract_flat': True,
        "playliststart": 1,
        "playlistend": 1000,
        "outtmpl": "%(id)s.%(ext)s",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)
        video_entries = playlist_info["entries"]
    return playlist_info, video_entries

def process_playlists(output_prefix):
    entries = []
    playlists = []
    playlists_data = get_all_playlists_data()
    for p in playlists_data:
        playlist_id = p["source_id"]
        _playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
        playlist_info, video_entries = get_playlist_data(_playlist_url)
        for video_entry in video_entries:
            video_entry['playlist_id'] = playlist_id
        entries.extend(video_entries)
        playlists.append(playlist_info)

    playlist_df = pd.DataFrame.from_dict(playlists, orient="columns")
    video_entries_df = pd.DataFrame(entries)

    playlist_df.to_excel(f'{output_prefix}_playlist_data.xlsx', sheet_name="Playlist Info", index=False)
    video_entries_df.to_excel(f'{output_prefix}_video_data.xlsx',  sheet_name="Video Entries", index=False)

    print("Playlist information and video entries exported.")

def download_file_from_r2(video_id, bucket_name, local_filename):
    file_key = f"iugaza1/{video_id}_raw.json"
    s3_client = boto3.client(
        service_name="s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        endpoint_url=ENDPOINT_URL
    )
    try:
        s3_client.download_file(bucket_name, file_key, local_filename)
        return True
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False