from fastapi import APIRouter, HTTPException, Request

from src.adapter.api.template.grade_level import GradeLevelCreate, GradeLevelUpdate

router = APIRouter(prefix="/grade-levels", tags=["grade-levels"])

@router.get("")
async def get_grade_levels(req: Request):
    repo = req.app.state.grade_level_repo
    return await repo.get_all()

@router.get("/{code}")
async def get_grade_level(code: str, req: Request):
    repo = req.app.state.grade_level_repo
    doc = await repo.get(code)
    if not doc:
        raise HTTPException(status_code=404, detail="Grade level not found")
    return doc.to_dict()

@router.post("")
async def create_grade_level(payload: GradeLevelCreate, req: Request):
    repo = req.app.state.grade_level_repo
    saved = await repo.add(payload.dict())
    if saved is None:
        raise HTTPException(status_code=409, detail="Already exists")
    return saved.to_dict()

@router.put("")
async def update_grade_level(payload: GradeLevelUpdate, req: Request):
    if not isinstance(payload.code, str):
        raise HTTPException(status_code=400, detail="Invalid ID")
    repo = req.app.state.grade_level_repo
    update_grade_level = await repo.update(payload.dict())
    if not update_grade_level:
        raise HTTPException(status_code=404, detail="GradeLevel not found")
    return update_grade_level.to_dict()

@router.delete("/{code}")
async def delete_grade_level(code: str, req: Request):
    repo = req.app.state.grade_level_repo
    return await repo.delete(code)