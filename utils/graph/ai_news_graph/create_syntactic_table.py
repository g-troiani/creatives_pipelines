import sqlite3
from utils.database.ai_news_database.create_tables import db_file

def create_syntactic_table():
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS syntactic (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id TEXT,
            sentence TEXT,
            dependencies TEXT,
            title TEXT,
            date TEXT,
            FOREIGN KEY (article_id) REFERENCES hacker_news (article_id)
        )
    ''')

    connection.commit()
    connection.close()
