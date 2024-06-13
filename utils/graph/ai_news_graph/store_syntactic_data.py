#
# UTILS/GRAPH/AI_NEWS_GRAPH/STORE_SYNTACTIC_DATA.PY
#

import sqlite3
from utils.database.ai_news_database.create_tables import db_file

def store_syntactic_data(article_id, sentence, dependencies, title, date):
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        query = '''
            INSERT INTO syntactic (article_id, sentence, dependencies, title, date)
            VALUES (?, ?, ?, ?, ?)
        '''
        values = (article_id, sentence, dependencies, title, date)
        cursor.execute(query, values)
        connection.commit()

        print(f"Stored syntactic data for article: {title}")

        cursor.close()
        connection.close()
    except sqlite3.Error as e:
        print(f'An error occurred while storing syntactic data: {e}')