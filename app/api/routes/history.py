from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.services.history_service import get_user_history, get_history_detail, delete_history
from app.utils.response import success_response


router = APIRouter(
    prefix="/history",
    tags=["History"]
)


@router.get("")
async def history(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),

    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    histories = await get_user_history(
        db=db,
        user_id=current_user.id,
        page=page,
        limit=limit
    )

    return success_response(
        message="History fetched successfully",
        data=histories
    )

@router.get("/{generation_id}")
async def history_detail(
    generation_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    generation = await get_history_detail(
        db=db,
        user_id=current_user.id,
        generation_id=generation_id
    )

    if not generation:
        raise HTTPException(
            status_code=404,
            detail="Generation not found"
        )

    return success_response(
        message="Generation detail fetched successfully",
        data=generation
    )

@router.delete("/{generation_id}")
async def remove_history(
    generation_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    generation = await delete_history(
        db=db,
        user_id=current_user.id,
        generation_id=generation_id
    )

    if not generation:
        raise HTTPException(
            status_code=404,
            detail="Generation not found"
        )

    return success_response(
        message="Generation deleted successfully",
        data=None
    )