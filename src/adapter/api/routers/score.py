from fastapi import APIRouter, HTTPException, Request

from src.adapter.api.template.score import ScoreCreate, ScoreUpdate

router = APIRouter(prefix="/scores", tags=["scores"])

@router.get("")
async def get_scores(req: Request):
    repo = req.app.state.score_repo
    return await repo.get_all()

@router.get("/{code}")
async def get_score(code: str, req: Request):
    repo = req.app.state.score_repo
    doc = await repo.get(code)
    if not doc:
        raise HTTPException(status_code=404, detail="Score not found")
    return doc.to_dict()

@router.post("")
async def create_score(payload: ScoreCreate, req: Request):
    repo = req.app.state.score_repo
    saved = await repo.add(payload.dict())
    if saved is None:
        raise HTTPException(status_code=409, detail="Already exists")
    return saved.to_dict()

@router.put("")
async def update_score(payload: ScoreUpdate, req: Request):
    if not isinstance(payload.code, str):
        raise HTTPException(status_code=400, detail="Invalid ID")
    repo = req.app.state.score_repo
    update_score = await repo.update(payload.dict())
    if not update_score:
        raise HTTPException(status_code=404, detail="Score not found")
    return update_score.to_dict()

@router.delete("/{code}")
async def delete_score(code: str, req: Request):
    repo = req.app.state.score_repo
    return await repo.delete(code)