import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import (
    hash_password,
    create_access_token,
    verify_password
)
from app.models.user import User
from app.schemas.auth import (
    RegisterRequest,
    AuthResponse,
    UserResponse,
    LoginRequest
)

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

@router.post(
    "/register",
    response_model=AuthResponse
)
async def register(
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    query = select(User).where(
        User.email == payload.email
    )

    result = await db.execute(query)

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(
        payload.password
    )

    new_user = User(
        id=str(uuid.uuid4()),
        name=payload.name,
        email=payload.email,
        password=hashed_password
    )

    db.add(new_user)

    await db.commit()

    token = create_access_token({
        "sub": new_user.id
    })

    return AuthResponse(
        token=token,
        user=UserResponse(
            id=new_user.id,
            name=new_user.name,
            email=new_user.email
        )
    )

@router.post(
    "/login",
    response_model=AuthResponse
)
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    query = select(User).where(
        User.email == payload.email
    )

    result = await db.execute(query)

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    is_valid_password = verify_password(
        payload.password,
        user.password
    )

    if not is_valid_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token({
        "sub": user.id
    })

    return AuthResponse(
        token=token,
        user=UserResponse(
            id=user.id,
            name=user.name,
            email=user.email
        )
    )