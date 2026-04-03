from fastapi import APIRouter, HTTPException, Request

from src.adapter.api.template.semester import SemesterCreate, SemesterUpdate

router = APIRouter(prefix="/semesters", tags=["semesters"])

@router.get("")
async def get_semesters(req: Request):
    repo = req.app.state.semester_repo
    return await repo.get_all()

@router.get("/{code}")
async def get_semester(code: str, req: Request):
    repo = req.app.state.semester_repo
    doc = await repo.get(code)
    if not doc:
        raise HTTPException(status_code=404, detail="Semester not found")
    return doc.to_dict()
@router.post("")
async def create_semester(payload: SemesterCreate, req: Request):
    repo = req.app.state.semester_repo
    saved = await repo.add(payload.dict())
    if saved is None:
        raise HTTPException(status_code=409, detail="Already exists")
    return saved.to_dict()

@router.put("")
async def update_semester(payload: SemesterUpdate, req: Request):
    if not isinstance(payload.code, str):
        raise HTTPException(status_code=400, detail="Invalid ID")
    repo = req.app.state.semester_repo
    update_semester = await repo.update(payload.dict())
    if not update_semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    return update_semester.to_dict()

@router.delete("/{code}")
async def delete_semester(code: str, req: Request):
    repo = req.app.state.semester_repo
    return await repo.delete(code)