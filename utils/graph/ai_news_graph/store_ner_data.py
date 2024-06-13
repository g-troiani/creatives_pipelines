#
# UTILS/GRAPH/AI_NEWS_GRAPH/STORE_NER_DATA.PY
#

import sqlite3
from utils.database.ai_news_database.create_tables import db_file

def store_ner_data(article_id, entity, count, title, date):
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        query = '''
            INSERT INTO ner (article_id, entity, count, title, date)
            VALUES (?, ?, ?, ?, ?)
        '''
        values = (article_id, entity, count, title, date)
        cursor.execute(query, values)
        connection.commit()

        print(f"Stored NER data for article: {title}")

        cursor.close()
        connection.close()
    except sqlite3.Error as e:
        print(f'An error occurred while storing NER data: {e}')