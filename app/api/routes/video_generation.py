from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.schemas.generation import GenerationRequest
from app.services.generation_service import generate_video_content
from app.utils.response import success_response


router = APIRouter(
    prefix="/generate",
    tags=["Video Generation"]
)


@router.post("")
async def generate_video(
    payload: GenerationRequest,
    current_user=Depends(get_current_user)
):
    result = await generate_video_content(payload)

    return success_response(
        message="Video generated successfully",
        data=result
    )