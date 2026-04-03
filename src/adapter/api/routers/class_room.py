from fastapi import APIRouter, HTTPException, Request

from src.adapter.api.template.class_room import ClassRoomCreate, ClassRoomUpdate

router = APIRouter(prefix="/classes", tags=["classes"])

@router.get("")
async def get_classes(req: Request):
    repo = req.app.state.class_room_repo
    return await repo.get_all()

@router.get("/{code}")
async def get_class(code: str, req: Request):
    repo = req.app.state.class_room_repo
    doc = await repo.get(code)
    if not doc:
        raise HTTPException(status_code=404, detail="Class not found")
    return doc.to_dict()

@router.post("")
async def create_class(payload: ClassRoomCreate, req: Request):
    repo = req.app.state.class_room_repo
    saved = await repo.add(payload.dict())
    if saved is None:
        raise HTTPException(status_code=409, detail="Already exists")
    return saved.to_dict()

@router.put("")
async def update_class(payload: ClassRoomUpdate, req: Request):
    if not isinstance(payload.code, str):
        raise HTTPException(status_code=400, detail="Invalid ID")
    repo = req.app.state.class_room_repo
    update_class = await repo.update(payload.dict())
    if not update_class:
        raise HTTPException(status_code=404, detail="Class not found")
    return update_class.to_dict()

@router.delete("/{code}")
async def delete_class(code: str, req: Request):
    repo = req.app.state.class_room_repo
    return await repo.delete(code)