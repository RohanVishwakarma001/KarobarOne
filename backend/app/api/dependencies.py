# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: api/dependencies.py — Shared API-Layer FastAPI Dependencies
# ================================================================================
# Why this file is used:
#   - It defines the shared DBSession type-alias used to inject database sessions
#     into API endpoint functions via dependency injection.
#
# What components are inside:
#   - DBSession  -> An Annotated type alias wrapping Depends(getDb), providing
#                   an active asynchronous database session parameter automatically.
# ================================================================================
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import getDb

DBSession = Annotated[AsyncSession, Depends(getDb)]