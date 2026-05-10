from http.client import HTTPException
import math

from sqlalchemy import desc, func, select

from app.models.generation import Generation


async def get_user_history(
    db,
    user_id,
    page: int = 1,
    limit: int = 10
):
    offset = (page - 1) * limit

    # get total count
    total_query = (
        select(func.count())
        .select_from(Generation)
        .where(Generation.user_id == user_id)
    )

    total_result = await db.execute(total_query)

    total = total_result.scalar()

    # get paginated data
    query = (
        select(Generation)
        .where(Generation.user_id == user_id)
        .order_by(desc(Generation.created_at))
        .offset(offset)
        .limit(limit)
    )

    result = await db.execute(query)

    items = result.scalars().all()

    total_pages = math.ceil(total / limit) if total > 0 else 1

    return {
        "items": items,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "next_page": page + 1 if page < total_pages else None,
            "previous_page": page - 1 if page > 1 else None
        }
    }

async def get_history_detail(
    db,
    user_id,
    generation_id
):
    query = (
        select(Generation)
        .where(
            Generation.id == generation_id,
            Generation.user_id == user_id
        )
    )

    result = await db.execute(query)

    return result.scalar_one_or_none()

async def delete_history(
    db,
    user_id,
    generation_id
):
    query = (
        select(Generation)
        .where(
            Generation.id == generation_id,
            Generation.user_id == user_id
        )
    )

    result = await db.execute(query)

    generation = result.scalar_one_or_none()

    if not generation:
        return None

    await db.delete(generation)

    await db.commit()

    return generation