# main.py

from src.etl import extract, transform, load
from src.ai import gemini
from src.database import get_db_connection, conn_sync
from src.utils import open_file
import os

def main():
    """Main function to run the entire pipeline."""
    print("Starting the IUG Course Transcripts pipeline...")

    # 1. Synchronize with the database
    conn_sync()

    # 2. Fetch playlist and video data from YouTube and save to Excel
    print("Fetching playlist data...")
    extract.process_playlists("new_iugaza1")

    # 3. Insert video data from Excel into the database
    print("Inserting video data into the database...")
    load.insert_videos_to_db("new_iugaza1_video_data.xlsx")

    # 4. Download raw transcripts from R2
    print("Downloading raw transcripts...")
    conn = get_db_connection()
    unsynced_videos = conn.execute("SELECT video_id, playlist_id FROM sync_github WHERE downloaded_r2 = 0 OR downloaded_r2 IS NULL").fetchall()
    for video_id, playlist_id in unsynced_videos:
        local_filename = f"data/raw/{playlist_id}/{video_id}_raw.json"
        if not os.path.exists(local_filename):
            os.makedirs(f"data/raw/{playlist_id}", exist_ok=True)
            if extract.download_file_from_r2(video_id, "youtube-iug-asdj", local_filename):
                load.update_downloaded_r2(video_id, playlist_id, 1)

    # 5. Process raw transcripts into SRT format and fix typos
    print("Processing transcripts...")
    for playlist_dir in os.scandir("data/raw"):
        if playlist_dir.is_dir():
            for raw_transcript_file in os.scandir(playlist_dir.path):
                if raw_transcript_file.name.endswith(".json"):
                    video_id = raw_transcript_file.name.replace("_raw.json", "")
                    processed_srt_path = f"data/processed/{playlist_dir.name}/{video_id}.srt"
                    final_srt_path = f"data/final/{playlist_dir.name}/{video_id}_clarified.srt"
                    
                    if not os.path.exists(processed_srt_path):
                        # This is a placeholder for the JSON to SRT conversion
                        # The original logic was complex and needs to be fully reimplemented
                        pass

                    if not os.path.exists(final_srt_path):
                        transform.fix_typos(processed_srt_path, final_srt_path)

    print("Pipeline finished.")

if __name__ == "__main__":
    main()