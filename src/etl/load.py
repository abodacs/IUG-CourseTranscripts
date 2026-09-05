import boto3
import pandas as pd
from ..database import get_db_connection
from ..config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    ENDPOINT_URL,
)

def upload_file_to_r2(file_path, bucket_name, object_key):
    s3 = boto3.client(
        service_name="s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        endpoint_url=ENDPOINT_URL
    )
    try:
        s3.upload_file(file_path, bucket_name, object_key)
        print(f"File uploaded successfully to R2 bucket: {bucket_name}, object key: {object_key}")
    except Exception as e:
        print(f"Error uploading file: {e}")

def update_downloaded_r2(video_id, playlist_id, status_flag):
    conn = get_db_connection()
    query = f"update sync_github set downloaded_r2 = {status_flag} where video_id= '{video_id}' and playlist_id='{playlist_id}';"
    conn.execute(query)
    conn.commit()
    conn.sync()

def insert_videos_to_db(excel_file):
    conn = get_db_connection()
    df = pd.read_excel(excel_file)
    error_ids = []
    for i, row in df.iterrows():
        video_id = row['id']
        playlist_id = row['playlist_id']
        try:
            conn.execute(f"INSERT INTO sync_github (video_id, playlist_id) VALUES ('{video_id}', '{playlist_id}');")
        except Exception as e:
            print(f"{str(e)=}")
            error_ids.append(video_id)
    conn.commit()
    conn.sync()
    print(f"Completed inserting videos. Errors: {error_ids}")