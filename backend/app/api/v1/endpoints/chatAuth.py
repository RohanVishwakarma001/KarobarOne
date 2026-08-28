# Owner: mousamdas156@gmail.com
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import getDb
from app.schemas.chatAuth import RegisterSchema, LoginSchema, TokenResponse
from app.services.authService import AuthService, UserRole
from app.db.models.chatUser import ChatUser

router = APIRouter(prefix="/chat-auth", tags=["Chat Authentication"])

@router.post("/register", response_model=TokenResponse)
async def register(data: RegisterSchema, session: AsyncSession = Depends(getDb)):
    user = await AuthService.register(
        session=session,
        name=data.name,
        email=data.email,
        password=data.password,
        role=data.role,
        storeId=data.storeId
    )
    return await AuthService.login(session, data.email, data.password)

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginSchema, session: AsyncSession = Depends(getDb)):
    return await AuthService.login(session, data.email, data.password)

@router.get("/users/lookup")
async def lookupUser(email: str, session: AsyncSession = Depends(getDb)):
    stmt = select(ChatUser).where(ChatUser.email == email)
    res = await session.execute(stmt)
    user = res.scalars().first()
    if not user:
        return {"found": False}
    return {
        "found": True,
        "userId": user.id,
        "name": user.name,
        "role": user.role
    }

@router.get("/stores/lookup")
async def lookupStore(storeId: int, session: AsyncSession = Depends(getDb)):
    stmt = select(ChatUser).where(ChatUser.storeId == storeId, ChatUser.role == UserRole.STORE_OWNER)
    res = await session.execute(stmt)
    owner = res.scalars().first()

    if not owner:
        return {"found": False}

    return {
        "found": True,
        "ownerName": owner.name,
        "userId": owner.id
    }