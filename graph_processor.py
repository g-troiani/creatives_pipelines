#
# GRAPH_PROCESSOR.PY
# 


import sqlite3
import logging
from ai_news_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, DB_FILE
from utils.ai_news_neo4j.neo4j_utils import Neo4jUtils
import datetime

logging.basicConfig(level=logging.INFO)

def process_graph_data():
    neo4j_utils = Neo4jUtils(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM youtube_videos")
        youtube_videos = cursor.fetchall()
        logging.info(f"Fetched {len(youtube_videos)} videos from the database")

        for video in youtube_videos:
            video_id = video[1]  # Assuming the video_id is in the second column
            title = video[2]  # Assuming the title is in the third column
            summary = video[6]  # Assuming the summary is in the seventh column

            logging.info(f"Adding nodes and relationships for video: {title}")

            neo4j_utils.add_node(video_id, title, summary, "YouTube Video")

            cursor.execute("SELECT * FROM ner WHERE article_id = ?", (video_id,))
            ner_data = cursor.fetchall()
            for ner in ner_data:
                entity = ner[1]
                count = ner[2]
                logging.info(f"Adding NER data to Neo4j: {entity}")
                neo4j_utils.store_ner_data(video_id, entity, count, title, datetime.now().strftime("%Y-%m-%d"))

            cursor.execute("SELECT * FROM ere WHERE article_id = ?", (video_id,))
            ere_data = cursor.fetchall()
            for ere in ere_data:
                entity = ere[1]
                relation = ere[2]
                target = ere[3]
                logging.info(f"Adding ERE data to Neo4j: {entity} -> {relation} -> {target}")
                neo4j_utils.store_ere_data(video_id, entity, relation, target, title, datetime.now().strftime("%Y-%m-%d"))

            cursor.execute("SELECT * FROM syntactic WHERE article_id = ?", (video_id,))
            syntactic_data = cursor.fetchall()
            for syntactic in syntactic_data:
                sentence = syntactic[1]
                dependencies = syntactic[2]
                logging.info(f"Adding Syntactic data to Neo4j: {sentence}")
                neo4j_utils.store_syntactic_data(video_id, sentence, dependencies, title, datetime.now().strftime("%Y-%m-%d"))

    neo4j_utils.close()

if __name__ == '__main__':
    process_graph_data()