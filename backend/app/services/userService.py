# Owner: mousamdas156@gmail.com
# ================================================================================
# Module: src/services/userService.py
# Purpose: User Management Service (CRUD & Business Rules)
# Last updated: 2026-07-11
# ================================================================================
"""
Service layer for User.
Handles user registration, profile updates, retrieval, and soft deletes.
"""

import uuid
from datetime import datetime, timezone
from typing import Sequence

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import AuthenticationError, ConflictError, NotFoundError
from app.db.models.user import User
from app.repositories.userRepository import UserRepository
from app.schemas.user import UserCreate, UserUpdate

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """
    Service class managing business logic for the global user base.
    """
    def __init__(self, session: AsyncSession):
        """
        Initialize the UserService.

        Purpose:
            Sets up the repository and DB session context.

        Parameters:
            session: Active database session.

        Return value:
            None
        """
        self.repo = UserRepository(session)
        self.session = session

    async def createUser(self, userPayload: UserCreate) -> User:
        """
        Registers a new user.

        Purpose:
            Performs email/mobile uniqueness verification, hashes passwords,
            and commits the new User record.

        Parameters:
            userPayload: Pydantic schema containing user registration details.

        Return value:
            The newly created User model instance.

        Exceptions:
            ConflictError: If the email or mobile already exists.
        """
        # 1. Enforce unique constraint on email
        if await self.repo.getByEmail(userPayload.email):
            raise ConflictError(
                f"User with email '{userPayload.email}' already exists"
            )
        # 2. Enforce unique constraint on mobile
        if await self.repo.getByMobile(userPayload.mobile):
            raise ConflictError(
                f"User with mobile '{userPayload.mobile}' already exists"
            )

        payload = userPayload.model_dump(exclude={"password"})
        user = User(
            **payload,
            passwordHash=pwdContext.hash(userPayload.password),
        )
        result = await self.repo.create(user)
        await self.session.commit()
        return result

    async def authenticate(self, email: str, password: str) -> User:
        """
        Verifies email/password credentials for login.

        Purpose:
            Looks up the user by email and checks the supplied password
            against the stored hash.

        Parameters:
            email: The user's email address.
            password: The plaintext password to verify.

        Return value:
            The matching, active User instance.

        Exceptions:
            AuthenticationError: If the credentials are invalid or the
                account is disabled/soft-deleted.
        """
        user = await self.repo.getByEmail(email)
        if not user or user.deletedAt is not None:
            raise AuthenticationError("Invalid email or password")
        if not pwdContext.verify(password, user.passwordHash):
            raise AuthenticationError("Invalid email or password")
        if not user.isActive:
            raise AuthenticationError("Account is disabled")
        return user

    async def markEmailVerified(self, userId: uuid.UUID) -> User:
        """
        Marks a user's email address as verified (after OTP verification).

        Exceptions:
            NotFoundError: If the user doesn't exist or is soft-deleted.
        """
        user = await self.repo.getById(userId)
        if not user or user.deletedAt is not None:
            raise NotFoundError("User", str(userId))
        result = await self.repo.update(user, {"isEmailVerified": True})
        await self.session.commit()
        return result

    async def recordLogin(self, userId: uuid.UUID) -> User:
        """
        Stamps 'lastLoginAt' after a successful OTP-verified login.

        Exceptions:
            NotFoundError: If the user doesn't exist or is soft-deleted.
        """
        user = await self.repo.getById(userId)
        if not user or user.deletedAt is not None:
            raise NotFoundError("User", str(userId))
        result = await self.repo.update(user, {"lastLoginAt": datetime.now(timezone.utc)})
        await self.session.commit()
        return result

    async def getUser(self, userId: uuid.UUID) -> User:
        """
        Gets a single active user by ID.

        Purpose:
            Retrieves an active (non-soft-deleted) user from database.

        Parameters:
            userId: UUID of the target user.

        Return value:
            The User model instance.

        Exceptions:
            NotFoundError: If the user doesn't exist or is soft-deleted.
        """
        user = await self.repo.getById(userId)
        if not user or user.deletedAt is not None:
            raise NotFoundError("User", str(userId))
        return user

    async def listUsers(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[Sequence[User], int]:
        """
        Lists users with server-side pagination.

        Purpose:
            Retrieves a paginated list of users and the total count.

        Parameters:
            skip: Count of records to skip.
            limit: Maximum count of records to return.

        Return value:
            A tuple of (list of users, total count).
        """
        return await self.repo.getAll(skip=skip, limit=limit)

    async def updateUser(
        self,
        userId: uuid.UUID,
        updatePayload: UserUpdate,
    ) -> User:
        """
        Updates profile fields of an existing user.

        Purpose:
            Modifies user fields while ensuring uniqueness constraints.

        Parameters:
            userId: UUID of the target user.
            updatePayload: Pydantic schema containing update details.

        Return value:
            The updated User model instance.

        Exceptions:
            NotFoundError: If the user doesn't exist or is soft-deleted.
            ConflictError: If email or mobile are modified to values already in use.
        """
        user = await self.repo.getById(userId)
        if not user or user.deletedAt is not None:
            raise NotFoundError("User", str(userId))

        updateData = updatePayload.model_dump(exclude_unset=True)
        if not updateData:
            return user

        # Check email uniqueness if email is being changed
        if "email" in updateData and updateData["email"] != user.email:
            existing = await self.repo.getByEmail(updateData["email"])
            if existing:
                raise ConflictError(
                    f"Email '{updateData['email']}' already in use"
                )

        # Check mobile uniqueness if mobile is being changed
        if "mobile" in updateData and updateData["mobile"] != user.mobile:
            existing = await self.repo.getByMobile(updateData["mobile"])
            if existing:
                raise ConflictError(
                    f"Mobile '{updateData['mobile']}' already in use"
                )

        result = await self.repo.update(user, updateData)
        await self.session.commit()
        return result

    async def deleteUser(self, userId: uuid.UUID) -> None:
        """
        Soft-deletes a user by stamping 'deletedAt'.

        Purpose:
            Excludes the user from login and active searches by soft-deletion.

        Parameters:
            userId: UUID of the target user.

        Return value:
            None

        Exceptions:
            NotFoundError: If the user doesn't exist or is already soft-deleted.
        """
        user = await self.repo.getById(userId)
        if not user or user.deletedAt is not None:
            raise NotFoundError("User", str(userId))
        await self.repo.update(user, {"deletedAt": datetime.now(timezone.utc)})
        await self.session.commit()