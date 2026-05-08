from fastapi import APIRouter, HTTPException, Request
from src.adapter.api.template.comment import Comment, AssessmentComment, SpecialAbilitiesComment

router = APIRouter(prefix="/student_assessment", tags=["student_assessment"])

@router.post("/comment")
async def add_comment(payload: AssessmentComment, req: Request):
    if not isinstance(payload.code, str):
        raise HTTPException(status_code=400, detail="Invalid ID")
    repo = req.app.state.core
    # repo.clear_student_assessment_outstanding(payload.code)
    result = None
    if payload.quality_comment:
        result = await repo.add_student_comment_general(Comment(
            code=payload.code,
            comment=payload.quality_comment
        ), "Phẩm chất")
    if payload.general_abilities_comment:
        result = await repo.add_student_comment_general(Comment(
            code=payload.code,
            comment=payload.general_abilities_comment
        ), "Năng lực chung")
    result = await repo.add_student_comment_special(SpecialAbilitiesComment(
        code=payload.code,
        vietnamese_comment=payload.vietnamese_comment,
        mathematics_comment=payload.mathematics_comment,
        informatics_comment=payload.informatics_comment,
        science_comment=payload.science_comment,
        history_and_geography_comment=payload.history_and_geography_comment,
        english_comment=payload.english_comment,
        technology_comment=payload.technology_comment,
        music_comment=payload.music_comment,
        arts_comment=payload.arts_comment,
        civics_comment=payload.civics_comment,
        physical_education_comment=payload.physical_education_comment,
        experiential_activities_comment=payload.experiential_activities_comment,
        nature_and_society_comment=payload.nature_and_society_comment,
    ))
    if not result:
        raise HTTPException(status_code=400, detail=f"comment is not useful for {payload.code}, please check logs")
    return result
