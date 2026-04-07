from fastapi import APIRouter, HTTPException, Request
from src.adapter.api.template.comment import Comment, AssessmentComment

router = APIRouter(prefix="/student_assessment", tags=["student_assessment"])

@router.post("/comment")
async def add_comment(payload: AssessmentComment, req: Request):
    if not isinstance(payload.code, str):
        raise HTTPException(status_code=400, detail="Invalid ID")
    repo = req.app.state.core
    # repo.clear_student_assessment_outstanding(payload.code)
    result = None
    if payload.quality_comment:
        result = await repo.add_student_comment(Comment(
            code=payload.code,
            comment=payload.quality_comment
        ), "Phẩm chất chủ yếu")
    if payload.general_abilities_comment:
        result = await repo.add_student_comment(Comment(
            code=payload.code,
            comment=payload.general_abilities_comment
        ), "Năng lực chung")
    if payload.special_abilities_comment:
        result = await repo.add_student_comment(Comment(
            code=payload.code,
            comment=payload.special_abilities_comment
        ), "Năng lực đặc thù")
    if not result:
        raise HTTPException(status_code=400, detail=f"comment is not useful for {payload.code}, please check logs")
    return result
