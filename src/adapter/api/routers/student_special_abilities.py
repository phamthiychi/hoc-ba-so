from fastapi import APIRouter, HTTPException, Request

router = APIRouter(prefix="/student_special_abilities", tags=["student_special_abilities"])

@router.post("/{commend}")
async def add_commend(code: str, commend: str, req: Request):
    if not isinstance(code, str):
        raise HTTPException(status_code=400, detail="Invalid ID")
    repo = req.app.state.core
    result = await repo.add_student_commend(code, commend, "Năng lực đặc thù")
    if not result:
        raise HTTPException(status_code=400, detail=f"Commend is not useful for {code}, please check logs")
    return result
