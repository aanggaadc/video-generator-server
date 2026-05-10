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