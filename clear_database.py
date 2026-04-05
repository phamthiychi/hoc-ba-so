
from src.adapter.database.postges_manager import postgres_manager
from src.adapter.database.mongo_manager import mongo_manager
from src.adapter.graph.neo4j_manager import neo4j_manager

postgres_manager.delete_db()
postgres_manager.create_db()

mongo_manager.clean_metadata_db("contact_infos")
mongo_manager.clean_metadata_db("subject_assessments")

neo4j_manager.clean_database()
