from fastapi import APIRouter, HTTPException, Request

from src.adapter.api.template.teaching_assignment import TeachingAssignmentCreate, TeachingAssignmentUpdate

router = APIRouter(prefix="/teaching-assignments", tags=["teaching-assignments"])

@router.get("/all")
async def get_teaching_assignments(req: Request):
    repo = req.app.state.teaching_assignment_repo
    return await repo.get_all()

@router.get("")
async def get_teaching_assignment(payload: TeachingAssignmentUpdate, req: Request):
    repo = req.app.state.teaching_assignment_repo
    code = await repo.create_code(payload.dict())
    doc = await repo.get(code)
    if not doc:
        raise HTTPException(status_code=404, detail="Teaching assignment not found")
    return doc.to_dict()

@router.post("")
async def create_teaching_assignment(payload: TeachingAssignmentCreate, req: Request):
    repo = req.app.state.teaching_assignment_repo
    saved = await repo.add(payload.dict())
    if saved is None:
        raise HTTPException(status_code=409, detail="Already exists")
    return saved.to_dict()

@router.put("")
async def update_teaching_assignment(payload: TeachingAssignmentUpdate, req: Request):
    repo = req.app.state.teaching_assignment_repo
    update_class = await repo.update(payload.dict())
    if not update_class:
        raise HTTPException(status_code=404, detail="Teaching assignment not found")
    return update_class.to_dict()

@router.delete("")
async def delete_teaching_assignment(payload: TeachingAssignmentUpdate, req: Request):
    repo = req.app.state.teaching_assignment_repo
    code = await repo.create_code(payload.dict())
    return await repo.delete(code)