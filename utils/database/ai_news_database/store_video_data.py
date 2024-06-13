#
# UTILS/DATABASE/AI_NEWS_DATABASE/STORE_VIDEO_DATA.PY
#

import sqlite3
from datetime import datetime
from utils.database.ai_news_database.create_tables import db_file

def store_video_data(video_id, title, channel_title, url, transcript, summary):
    """
    Store the video data in the database.
    
    Args:
        video_id (str): The ID of the video.
        title (str): The title of the video.
        channel_title (str): The title of the channel.
        url (str): The URL of the video.
        transcript (str): The transcript of the video.
        summary (str): The summary of the video.
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Check if the video already exists in the database
    cursor.execute("SELECT id FROM youtube_videos WHERE video_id = ?", (video_id,))
    result = cursor.fetchone()

    if result is None:
        # Insert the video into the database
        cursor.execute("""
            INSERT INTO youtube_videos (video_id, title, channel_title, url, transcript, summary, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            video_id,
            title,
            channel_title,
            url,
            transcript,
            summary,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        print(f"Inserted video: {title}")
    else:
        print(f"Video already exists in the database: {title}")

    conn.commit()
    conn.close()