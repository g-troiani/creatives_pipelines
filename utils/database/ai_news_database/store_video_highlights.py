#
# UTILS/DATABASE/AI_NEWS_DATABASE/STORE_VIDEO_HIGHLIGHTS.PY
#

import sqlite3
from utils.database.ai_news_database.create_tables import db_file

def store_video_highlights(video_id, highlights, translated_highlights):
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        query = '''
            INSERT INTO video_highlights (video_id, highlights, translated_highlights)
            VALUES (?, ?, ?)
        '''
        values = (video_id, highlights, translated_highlights)
        cursor.execute(query, values)
        connection.commit()
        print(f"Stored highlights for video: {video_id}")
        cursor.close()
        connection.close()
    except sqlite3.Error as e:
        print(f'An error occurred while storing video highlights: {e}')