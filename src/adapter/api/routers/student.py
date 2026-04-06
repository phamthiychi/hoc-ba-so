from typing import List
from fastapi import APIRouter, HTTPException, Request, UploadFile, File, Form

from src.adapter.api.template.student_records import StudentRecords
from src.adapter.api.template.student import StudentUpdate

router = APIRouter(prefix="/students", tags=["students"])

@router.get("")
async def find_students(req: Request):
    repo = req.app.state.student_repo
    return await repo.find_students()

@router.get("/{code}")
async def find_student(code: str, req: Request):
    if not isinstance(code, str):
        raise HTTPException(status_code=400, detail="Invalid ID")
    repo = req.app.state.core
    doc = await repo.find_student(code)
    if not doc:
        raise HTTPException(status_code=404, detail="Student not found")
    return doc

@router.post("")
async def add_student(
    req: Request,
    academic_year: str = Form(...),
    file_profiles: UploadFile = File(...)
):
    if file_profiles.filename != "" and not file_profiles.filename.endswith(".xls"):
        raise HTTPException(status_code=400, detail="Profile file only .xls allowed")
    repo = req.app.state.core
    result = await repo.add_student(StudentRecords(
        academic_year=academic_year,
        file_profiles=None if file_profiles.filename == "" else file_profiles
    ))
    if not result:
        return {"message": "created"}
    raise HTTPException(status_code=400, detail=f"Can not add {result}, please check logs")

@router.put("")
async def update_student(payload: StudentUpdate, req: Request):
    if not isinstance(payload.code, str):
        raise HTTPException(status_code=400, detail="Invalid ID")
    repo = req.app.state.student_repo
    update_student = await repo.update_student(payload)
    if not update_student:
        raise HTTPException(status_code=404, detail=f"Student {payload.code} not found")
    return update_student.to_dict()

@router.delete("/{code}")
async def delete_student(code :str, req: Request):
    if not isinstance(code, str):
        raise HTTPException(status_code=400, detail="Invalid ID")
    repo = req.app.state.student_repo
    if await repo.delete_student(code):
        return {"message": "ok"}
    raise HTTPException(status_code=404, detail=f"Error when delete student's code {code}, please check logs")
