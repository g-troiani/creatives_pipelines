#
# UTILS/GRAPH/AI_NEWS_GRAPH/CREATE_NER_TABLE.PY
#

import sqlite3
from utils.database.ai_news_database.create_tables import db_file

def create_ner_table():
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ner (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id TEXT,
            entity TEXT,
            count INTEGER,
            title TEXT,
            date TEXT,
            FOREIGN KEY (article_id) REFERENCES hacker_news (article_id)
        )
    ''')

    connection.commit()
    connection.close()
