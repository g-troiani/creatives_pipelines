import sqlite3
from datetime import datetime

def store_videos_in_database(videos):
    """
    Store the retrieved videos and their summaries in the database.
    
    Args:
        videos (list): A list of dictionaries containing the video information.
    """
    conn = sqlite3.connect("data/ai_news.db")
    cursor = conn.cursor()

    for video in videos:
        # Check if the video already exists in the database
        cursor.execute("SELECT id FROM youtube_videos WHERE video_id = ?", (video["Video ID"],))
        result = cursor.fetchone()

        if result is None:
            # Insert the video into the database
            cursor.execute("""
                INSERT INTO youtube_videos (video_id, title, description, summary, url, published_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                video["Video ID"],
                video["Title"],
                video["Description"],
                video["Summary"],
                video["URL"],
                video["Published At"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            print(f"Inserted video: {video['Title']}")

            # Extract entities and their counts from the NER result
            entities = video["NER"].split("\n\n")
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
                    values = (video["Video ID"], entity_name, entity_count, video["Title"], datetime.now().strftime("%Y-%m-%d"))
                    cursor.execute(query, values)

            # Extract entities, relations, and targets from the ERE result
            ere_triples = video["ERE"].split("\n\n")
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
                    values = (video["Video ID"], entity, relation, target, video["Title"], datetime.now().strftime("%Y-%m-%d"))
                    cursor.execute(query, values)

            # Extract sentences and their dependencies from the syntactic result
            syntactic_data = video["Syntactic"].split("\n\n")
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
                    values = (video["Video ID"], sentence, dependencies, video["Title"], datetime.now().strftime("%Y-%m-%d"))
                    cursor.execute(query, values)
        else:
            print(f"Video already exists in the database: {video['Title']}")

    conn.commit()
    conn.close()
