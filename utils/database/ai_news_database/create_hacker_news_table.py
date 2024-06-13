#
# UTILS/DATABASE/AI_NEWS_DATABASE/CREATE_HACKER_NEWS_TABLE.PY
#

import sqlite3
from utils.database.ai_news_database.create_tables import db_file

def create_hacker_news_table():
    """
    Create the hacker_news table in the database if it doesn't exist.
    """
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS hacker_news')  # Drop the existing table if it exists

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hacker_news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id TEXT UNIQUE,
            text TEXT,
            summary TEXT,
            url TEXT,
            page_url TEXT,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    connection.commit()
    connection.close()
