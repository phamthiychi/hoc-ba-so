from fastapi import FastAPI, Request
from sqlalchemy import text

from src.adapter.database.postges_manager import postgres_manager
from src.adapter.database.mongo_manager import mongo_manager
from src.adapter.graph.neo4j_manager import neo4j_manager
from src.application.core import SystemCore
from src.application.utils import Utils

from src.adapter.api.routers.student import router as student_router
from src.adapter.api.routers.student_contact_infos import router as student_contact_infos_router
from src.adapter.api.routers.student_subject_assessments import router as student_subject_assessments_router
from src.adapter.api.routers.student_assessment import router as student_assessment_router

app = FastAPI(title="HOCBASO API")

@app.on_event("startup")
async def startup():
    session = postgres_manager.session
    db = mongo_manager.get_metadata_db()
    manager = neo4j_manager
    app.state.core = SystemCore(session, db, manager)
    app.state.utils = Utils()

@app.get("/health")
async def health():
    try:
        postgres_manager.session.execute(text("SELECT 1"))
        print("✅ Database connected")
        return {
            "status": "200 ok",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "504 error",
            "database": "disconnected",
            "error": e
        }
    finally:
        postgres_manager.session.close()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    app.state.utils._log(f"Status: 500 error, {exc}")

app.include_router(student_router)
app.include_router(student_contact_infos_router)
app.include_router(student_subject_assessments_router)
app.include_router(student_assessment_router)
