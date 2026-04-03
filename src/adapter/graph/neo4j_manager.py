from typing import Any, Callable, List, Optional
from neo4j import GraphDatabase
from src.common.ontology_setting import settings


class Neo4jManager:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_DB_URI,
            auth=(settings.NEO4J_DB_USER, settings.NEO4J_DB_PASSWORD)
        )

    def check_neo4j_connection(self):
        try:
            self.driver.verify_connectivity()
            print("✅ Kết nối thành công tới Neo4j!")
        except Exception as e:
            print(f"❌ Kết nối thất bại: {e}")

    def close(self):
        self.driver.close()

    def execute_write(self, callback: Callable, *args, **kwargs):
        with self.driver.session(database=settings.NEO4J_DB) as session:
            return session.execute_write(callback, *args, **kwargs)

    def execute_read(self, callback: Callable, *args, **kwargs):
        with self.driver.session(database=settings.NEO4J_DB) as session:
            return session.execute_read(callback, *args, **kwargs)

    def clean_database(self):
        with self.driver.session(database=settings.NEO4J_DB) as session:
            session.execute_write(self._delete_all)

    @staticmethod
    def _delete_all(tx):
        tx.run("MATCH (n) DETACH DELETE n")

neo4j_manager = Neo4jManager()
