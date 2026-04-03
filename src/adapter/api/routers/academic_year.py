from fastapi import APIRouter, HTTPException, Request

from src.adapter.api.template.academic_year import AcademicYearCreate, AcademicYearUpdate

router = APIRouter(prefix="/academic-years", tags=["academic-years"])

@router.get("")
async def get_academic_years(req: Request):
    repo = req.app.state.academic_year_repo
    return await repo.get_all()

@router.get("/{code}")
async def get_academic_year(code: str, req: Request):
    repo = req.app.state.academic_year_repo
    doc = await repo.get(code)
    if not doc:
        raise HTTPException(status_code=404, detail="Academic year not found")
    return doc.to_dict()

@router.post("")
async def create_academic_year(payload: AcademicYearCreate, req: Request):
    repo = req.app.state.academic_year_repo
    saved = await repo.add(payload.dict())
    if saved is None:
        raise HTTPException(status_code=409, detail="Already exists")
    return saved.to_dict()


@router.put("")
async def update_academic_year(payload: AcademicYearUpdate, req: Request):
    if not isinstance(payload.code, str):
        raise HTTPException(status_code=400, detail="Invalid ID")
    repo = req.app.state.academic_year_repo
    update_academic_year = await repo.update(payload.dict())
    if not update_academic_year:
        raise HTTPException(status_code=404, detail="AcademicYear not found")
    return update_academic_year.to_dict()

@router.delete("/{code}")
async def delete_academic_year(code: str, req: Request):
    repo = req.app.state.academic_year_repo
    return await repo.delete(code)