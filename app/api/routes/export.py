from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.models.generation import Generation

from app.services.export_service import (
    build_txt_export,
    build_json_export,
)

router = APIRouter(
    prefix="/export",
    tags=["Export"],
)

@router.get("/{generation_id}")
async def export_generation(
    generation_id: UUID,
    format: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Generation).where(
        Generation.id == generation_id,
        Generation.user_id == current_user.id,
    )

    result = await db.execute(query)

    generation = result.scalar_one_or_none()

    if not generation:
        raise HTTPException(
            status_code=404,
            detail="Generation not found",
        )

    filename = (
        generation.generated_title
        or "video-generation"
    )

    filename = filename.replace(" ", "-").lower()

    if format == "txt":
        content = build_txt_export(generation)

        return Response(
            content=content,
            media_type="text/plain",
            headers={
                "Content-Disposition":
                f"attachment; filename={filename}.txt"
            },
        )

    elif format == "json":
        content = build_json_export(generation)

        return Response(
            content=content,
            media_type="application/json",
            headers={
                "Content-Disposition":
                f"attachment; filename={filename}.json"
            },
        )

    raise HTTPException(
        status_code=400,
        detail="Invalid export format",
    )