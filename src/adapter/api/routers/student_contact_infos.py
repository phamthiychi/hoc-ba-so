from fastapi import APIRouter, HTTPException, Request

router = APIRouter(prefix="/student_contact_infos", tags=["student_contact_infos"])

@router.get("/{code}")
async def get_student_contact_infos(code: str, req: Request):
    if not isinstance(code, str):
        raise HTTPException(status_code=400, detail="Invalid ID")
    repo = req.app.state.core
    doc = await repo.find_student_contact_infos(code)
    if not doc:
        raise HTTPException(status_code=404, detail="Student contact not found")
    return doc
