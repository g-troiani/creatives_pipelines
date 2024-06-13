#
# UTILS/DATABASE/AI_NEWS_DATABASE/CREATE_TABLES.PY
#


import sqlite3

db_file = "data/ai_news.db"

def create_tables():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create the youtube_videos table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS youtube_videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT UNIQUE,
            title TEXT,
            channel_title TEXT,
            url TEXT,
            transcript TEXT,
            timestamps TEXT,
            summary TEXT,
            created_at TIMESTAMP
        )
    """)

    # Create the hacker_news table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hacker_news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id TEXT UNIQUE,
            text TEXT,
            summary TEXT,
            url TEXT,
            page_url TEXT,
            title TEXT,
            created_at TIMESTAMP
        )
    """)

    # Create the daily_report table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_report (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            report_path TEXT,
            created_at TIMESTAMP
        )
    """)

    # Create the techcrunch table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS techcrunch_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT UNIQUE,
            text TEXT,
            summary TEXT,
            timestamp TEXT,
            created_at TIMESTAMP
        )
    """)

    # Create the video_highlights table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS video_highlights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            highlights TEXT,
            translated_highlights TEXT,
            created_at TIMESTAMP,
            FOREIGN KEY (video_id) REFERENCES youtube_videos (video_id)
        )
    """)

    # Create the social_media_content table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS social_media_content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_url TEXT,
            video_title TEXT,
            channel_title TEXT,
            english_highlights TEXT,
            spanish_highlights TEXT,
            video_date TEXT,
            created_at TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

__all__ = ['create_tables', 'db_file']