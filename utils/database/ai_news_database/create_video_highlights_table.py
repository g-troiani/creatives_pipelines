import sqlite3
from utils.database.ai_news_database.create_tables import db_file

def create_video_highlights_table():
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS video_highlights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            highlights TEXT,
            translated_highlights TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (video_id) REFERENCES videos (video_id)
        )
    ''')
    connection.commit()
    connection.close()