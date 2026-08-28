# Owner: mousamdas156@gmail.com
# ================================================================================
# Module: src/api/v1/endpoints/users.py
# Purpose: Router layer for User
# Last updated: 2026-07-11
# ================================================================================
"""
Router layer for User.
Exposes registration, retrieval, listing, update, and soft-delete endpoints.
"""

import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import getCurrentUserId
from app.core.rbac import Roles, require_role
from app.db.session import getDb
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.userService import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(Roles.PLATFORM_OWNER, Roles.STORE_OWNER, Roles.STORE_ADMIN))],
)
async def createUser(
    userPayload: UserCreate,
    session: AsyncSession = Depends(getDb),
) -> UserResponse:
    """
    Register a new user.

    Purpose:
        Endpoint to create a new user.

    Parameters:
        userPayload: The Pydantic model for user registration.
        session: Database session dependency.

    Return value:
        The response representation of the created user.
    """
    service = UserService(session)
    return await service.createUser(userPayload)


@router.get(
    "/{userId}",
    response_model=UserResponse,
    dependencies=[Depends(getCurrentUserId)],
)
async def getUser(
    userId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
) -> UserResponse:
    """
    Get an active user by ID.

    Purpose:
        Endpoint to retrieve a user's details.

    Parameters:
        userId: The UUID of the user.
        session: Database session dependency.

    Return value:
        The details of the user.
    """
    service = UserService(session)
    return await service.getUser(userId)


@router.get(
    "/",
    response_model=list[UserResponse],
    dependencies=[Depends(getCurrentUserId)],
)
async def listUsers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(getDb),
) -> list[UserResponse]:
    """
    List users with pagination.

    Purpose:
        Endpoint to retrieve a paginated list of users.

    Parameters:
        skip: Count of records to skip.
        limit: Max count of records to return.
        session: Database session dependency.

    Return value:
        A list of user response objects.
    """
    service = UserService(session)
    users, _total = await service.listUsers(skip=skip, limit=limit)
    return users


@router.patch(
    "/{userId}",
    response_model=UserResponse,
    dependencies=[Depends(getCurrentUserId)],
)
async def updateUser(
    userId: uuid.UUID,
    updatePayload: UserUpdate,
    session: AsyncSession = Depends(getDb),
) -> UserResponse:
    """
    Update an existing user.

    Purpose:
        Endpoint to modify user fields.

    Parameters:
        userId: The UUID of the user.
        updatePayload: The Pydantic model containing updates.
        session: Database session dependency.

    Return value:
        The updated user details.
    """
    service = UserService(session)
    return await service.updateUser(userId, updatePayload)


@router.delete(
    "/{userId}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(Roles.PLATFORM_OWNER, Roles.STORE_OWNER))],
)
async def deleteUser(
    userId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
) -> None:
    """
    Soft-delete a user.

    Purpose:
        Endpoint to soft-delete a user.

    Parameters:
        userId: The UUID of the user.
        session: Database session dependency.

    Return value:
        None
    """
    service = UserService(session)
    await service.deleteUser(userId)

