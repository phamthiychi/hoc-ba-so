from fastapi import APIRouter, HTTPException, Request

from src.adapter.api.template.teacher import TeacherCreate, TeacherUpdate

router = APIRouter(prefix="/teachers", tags=["teachers"])

@router.get("")
async def get_teachers(req: Request):
    repo = req.app.state.teacher_repo
    return await repo.get_all()

@router.get("/{code}")
async def get_teacher(code: str, req: Request):
    if not isinstance(code, str):
        raise HTTPException(status_code=400, detail="Invalid code")
    repo = req.app.state.teacher_repo
    doc = await repo.get(code)
    if not doc:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return doc.to_dict()

@router.post("")
async def create_teacher(payload: TeacherCreate, req: Request):
    repo = req.app.state.teacher_repo
    saved = await repo.add(payload.dict())
    if saved is None:
        raise HTTPException(status_code=409, detail="Already exists")
    return saved.to_dict()

@router.put("")
async def update_teacher(payload: TeacherUpdate, req: Request):
    if not isinstance(payload.code, str):
        raise HTTPException(status_code=400, detail="Invalid code")
    repo = req.app.state.teacher_repo
    updated_teacher = await repo.update(payload.dict())
    if not updated_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return updated_teacher.to_dict()

@router.delete("/{code}")
async def delete_teacher(code: str, req: Request):
    if not isinstance(code, str):
        raise HTTPException(status_code=400, detail="Invalid code")
    repo = req.app.state.teacher_repo
    return await repo.delete(code)