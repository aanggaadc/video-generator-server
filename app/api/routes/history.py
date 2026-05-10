from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.services.history_service import get_user_history
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