#
# UTILS/DATABASE/AI_NEWS_DATABASE/CREATE_TECHCRUNCH_TABLE.PY
#
 
import sqlite3
from utils.database.ai_news_database.create_tables import db_file

def create_techcrunch_table():
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS techcrunch_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id TEXT UNIQUE,
            title TEXT,
            url TEXT,
            text TEXT,
            summary TEXT,
            timestamp TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    connection.commit()
    connection.close()
