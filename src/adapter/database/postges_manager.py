from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.model.postgres.base import Base

import src.model.postgres.academic_year
import src.model.postgres.grade_level
import src.model.postgres.class_room
import src.model.postgres.score
import src.model.postgres.semester
import src.model.postgres.student
import src.model.postgres.subject
import src.model.postgres.teacher
import src.model.postgres.learning_result
import src.model.postgres.teaching_assignment

from src.common.connect_setting import settings
class PostgresManager:
    def __init__(self):
        URI = settings.POSTGRES_DB_URI
        self.engine = create_engine(URI, echo=True)
        SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
        self.session = SessionLocal()
        self.tables_enable_rls = [
            "academic_year",
            "learning_result",
            "class_room",
            "grade_level",
            "score",
            "semester",
            "student",
            "subject",
            "teacher",
            "teaching_assignment"
        ]

    def create_db(self):
        Base.metadata.create_all(self.engine)
        with self.engine.connect() as conn:
            for table in self.tables_enable_rls:
                conn.execute(text(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;"))
            conn.commit()
        print("Tables created + RLS enabled")
        print("Tables created")

    def delete_db(self):
        Base.metadata.drop_all(self.engine)
        print("All tables dropped")

    def clean_data(self, table_name):
        table = Base.metadata.tables.get(table_name)
        if table is not None:
            self.session.execute(table.delete())
            self.session.commit()

postgres_manager = PostgresManager()
