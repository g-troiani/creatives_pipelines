#
# UTILS/GRAPH/AI_NEWS_GRAPH/CREATE_ERE_DATA.PY
#

import sqlite3
from utils.database.ai_news_database.create_tables import db_file

def store_ere_data(article_id, entity, relation, target, title, date):
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        query = '''
            INSERT INTO ere (article_id, entity, relation, target, title, date)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        values = (article_id, entity, relation, target, title, date)
        cursor.execute(query, values)
        connection.commit()

        print(f"Stored ERE data for article: {title}")

        cursor.close()
        connection.close()
    except sqlite3.Error as e:
        print(f'An error occurred while storing ERE data: {e}')