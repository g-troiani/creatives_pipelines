#
# UTILS/AI_NEWS_NEO4J/NEO4J_UTILS.PY
#


#
# UTILS/AI_NEWS_NEO4J/NEO4J_UTILS.PY
#


from neo4j import GraphDatabase

class Neo4jUtils:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_node(self, node_id, title, summary, label):
        with self.driver.session() as session:
            session.run(
                "MERGE (n:{} {{id: '{}', title: '{}', summary: '{}'}})".format(
                    label, node_id, title, summary
                )
            )

    def add_relationship(self, source_id, relationship_type, target_id):
        with self.driver.session() as session:
            session.run(
                "MATCH (a), (b) WHERE a.id = '{}' AND b.id = '{}' MERGE (a)-[r:{}]->(b)".format(
                    source_id, target_id, relationship_type
                )
            )

    def store_ner_data(self, article_id, entity, count, title, date):
        with self.driver.session() as session:
            session.run("""
                MERGE (a:Article {id: $article_id, title: $title, date: $date})
                MERGE (e:Entity {name: $entity})
                MERGE (a)-[r:MENTIONS]->(e)
                ON CREATE SET r.count = $count
                ON MATCH SET r.count = r.count + $count
            """, article_id=article_id, entity=entity, count=count, title=title, date=date)

    def store_ere_data(self, article_id, entity, relation, target, title, date):
        with self.driver.session() as session:
            session.run("""
                MERGE (a:Article {id: $article_id, title: $title, date: $date})
                MERGE (e:Entity {name: $entity})
                MERGE (t:Entity {name: $target})
                MERGE (e)-[r:RELATION {type: $relation}]->(t)
            """, article_id=article_id, entity=entity, relation=relation, target=target, title=title, date=date)

    def store_syntactic_data(self, article_id, sentence, dependencies, title, date):
        with self.driver.session() as session:
            session.run("""
                MERGE (a:Article {id: $article_id, title: $title, date: $date})
                MERGE (s:Sentence {text: $sentence})
                MERGE (a)-[r:CONTAINS]->(s)
                SET s.dependencies = $dependencies
            """, article_id=article_id, sentence=sentence, dependencies=dependencies, title=title, date=date)

    def migrate_ner_data_from_sqlite(self, sqlite_connection):
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT article_id, entity, count, title, date FROM ner")
        ner_data = cursor.fetchall()
        with self.driver.session() as session:
            for article_id, entity, count, title, date in ner_data:
                session.run("""
                    MERGE (a:Article {id: $article_id, title: $title, date: $date})
                    MERGE (e:Entity {name: $entity})
                    MERGE (a)-[r:MENTIONS]->(e)
                    ON CREATE SET r.count = $count
                    ON MATCH SET r.count = r.count + $count
                """, article_id=article_id, entity=entity, count=count, title=title, date=date)
        cursor.execute("DELETE FROM ner")
        sqlite_connection.commit()

    def migrate_ere_data_from_sqlite(self, sqlite_connection):
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT article_id, entity, relation, target, title, date FROM ere")
        ere_data = cursor.fetchall()
        with self.driver.session() as session:
            for article_id, entity, relation, target, title, date in ere_data:
                session.run("""
                    MERGE (a:Article {id: $article_id, title: $title, date: $date})
                    MERGE (e:Entity {name: $entity})
                    MERGE (t:Entity {name: $target})
                    MERGE (e)-[r:RELATION {type: $relation}]->(t)
                """, article_id=article_id, entity=entity, relation=relation, target=target, title=title, date=date)
        cursor.execute("DELETE FROM ere")
        sqlite_connection.commit()

    def migrate_syntactic_data_from_sqlite(self, sqlite_connection):
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT article_id, sentence, dependencies, title, date FROM syntactic")
        syntactic_data = cursor.fetchall()
        with self.driver.session() as session:
            for article_id, sentence, dependencies, title, date in syntactic_data:
                session.run("""
                    MERGE (a:Article {id: $article_id, title: $title, date: $date})
                    MERGE (s:Sentence {text: $sentence})
                    MERGE (a)-[r:CONTAINS]->(s)
                    SET s.dependencies = $dependencies
                """, article_id=article_id, sentence=sentence, dependencies=dependencies, title=title, date=date)
        cursor.execute("DELETE FROM syntactic")
        sqlite_connection.commit()