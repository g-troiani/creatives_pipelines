#
# SCRAPERS/AI_NEWS_SCRAPERS/TECHCRUNCH_SCRAPER/STORE_ARTICLES_IN_DATABASE.PY
# 

import sqlite3
from datetime import datetime

def store_articles_in_database(articles):
    """
    Store the retrieved articles and their summaries in the database.
    
    Args:
        articles (list): A list of dictionaries containing the article information.
    """
    conn = sqlite3.connect("data/ai_news.db")
    cursor = conn.cursor()

    for article in articles:
        # Check if the article already exists in the database
        cursor.execute("SELECT id FROM techcrunch_articles WHERE url = ?", (article["URL"],))
        result = cursor.fetchone()

        if result is None:
            # Insert the article into the database
            cursor.execute("""
                INSERT INTO techcrunch_articles (title, url, text, summary, timestamp, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                article["Title"],
                article["URL"],
                article["Text"],
                article["Summary"],
                article["Timestamp"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            print(f"Inserted article: {article['Title']}")

            # Extract entities and their counts from the NER result
            entities = article["NER"].split("\n\n")
            for entity in entities:
                if "Entity:" in entity:
                    entity_parts = entity.split("\n")
                    entity_name = entity_parts[0].replace("Entity: ", "")
                    entity_count = int(entity_parts[1].replace("Count: ", ""))

                    # Insert the entity, count, title, and date into the ner table
                    query = '''
                        INSERT INTO ner (article_id, entity, count, title, date)
                        VALUES (?, ?, ?, ?, ?)
                    '''
                    values = (article["URL"], entity_name, entity_count, article["Title"], datetime.now().strftime("%Y-%m-%d"))
                    cursor.execute(query, values)

            # Extract entities, relations, and targets from the ERE result
            ere_triples = article["ERE"].split("\n\n")
            for triple in ere_triples:
                if "Entity:" in triple:
                    triple_parts = triple.split("\n")
                    entity = triple_parts[0].replace("Entity: ", "")
                    relation = triple_parts[1].replace("Relation: ", "")
                    target = triple_parts[2].replace("Target: ", "")

                    # Insert the entity, relation, target, title, and date into the ere table
                    query = '''
                        INSERT INTO ere (article_id, entity, relation, target, title, date)
                        VALUES (?, ?, ?, ?, ?, ?)
                    '''
                    values = (article["URL"], entity, relation, target, article["Title"], datetime.now().strftime("%Y-%m-%d"))
                    cursor.execute(query, values)

            # Extract sentences and their dependencies from the syntactic result
            syntactic_data = article["Syntactic"].split("\n\n")
            for data in syntactic_data:
                if "Sentence:" in data:
                    data_parts = data.split("\n")
                    sentence = data_parts[0].replace("Sentence: ", "")
                    dependencies = data_parts[1].replace("Dependencies: ", "")

                    # Insert the sentence, dependencies, title, and date into the syntactic table
                    query = '''
                        INSERT INTO syntactic (article_id, sentence, dependencies, title, date)
                        VALUES (?, ?, ?, ?, ?)
                    '''
                    values = (article["URL"], sentence, dependencies, article["Title"], datetime.now().strftime("%Y-%m-%d"))
                    cursor.execute(query, values)
        else:
            print(f"Article already exists in the database: {article['Title']}")

    conn.commit()
    conn.close()
