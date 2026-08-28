# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: db/session.py — Async Database Engine, Session Factory & FastAPI Dependency
# ================================================================================
# Why this file is used:
#   - It manages async engines, pool policies, and session allocations.
#
# What components are inside:
#   - getEngine()          -> Returns the async SQLAlchemy engine singleton.
#   - getSessionFactory()  -> Returns the async session factory singleton.
#   - getDb()              -> Async generator dependency injecting sessions with auto-commits/rollbacks.
# ================================================================================
"""
Async database engine, session factory, and FastAPI dependency.

Connection pool is configured with:
  - pool_size: Base number of reusable connections
  - max_overflow: Extra connections for traffic spikes
  - pool_recycle: Recycle stale connections (prevents PostgreSQL timeouts)
  - pool_pre_ping: Verify connection is alive before handing it out
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import getSettings

# ──────────────────────────────────────────────
# Lazy-initialized singletons
# ──────────────────────────────────────────────

_engine: AsyncEngine | None = None
_asyncSessionFactory: async_sessionmaker[AsyncSession] | None = None


def getEngine() -> AsyncEngine:
    """
    Return the async SQLAlchemy engine (created lazily on first call).

    Pool settings are loaded from pydantic-settings configuration.
    """
    global _engine
    if _engine is None:
        settings = getSettings()
        _engine = create_async_engine(
            settings.databaseUrl,
            echo=settings.debug,
            pool_size=settings.dbPoolSize,
            max_overflow=settings.dbMaxOverflow,
            pool_timeout=settings.dbPoolTimeout,
            pool_recycle=settings.dbPoolRecycle,
            pool_pre_ping=True,
        )
    return _engine



def getSessionFactory() -> async_sessionmaker[AsyncSession]:
    """Return the async session factory (created lazily on first call)."""
    global _asyncSessionFactory
    if _asyncSessionFactory is None:
        _asyncSessionFactory = async_sessionmaker(
            bind=getEngine(),
            class_=AsyncSession,
            expire_on_commit=False,  # Critical for async — prevents detached object errors
        )
    return _asyncSessionFactory


async def getDb() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides an async database session.

    Usage:
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(getDb)):
            ...

    The session is automatically committed on success and rolled back on error.
    If a tenant ID is set in the request ContextVar, sets the DB session GUC.
    """
    from app.core.tenant import getCurrentTenantId
    from sqlalchemy import text

    sessionFactory = getSessionFactory()
    async with sessionFactory() as session:
        tenant_id = getCurrentTenantId()
        if tenant_id:
            try:
                await session.execute(
                    text("SELECT set_config('app.current_tenant_id', :tid, true)"),
                    {"tid": str(tenant_id)},
                )
            except Exception:
                # SET LOCAL failure aborts the PostgreSQL transaction.
                # Roll back so subsequent queries can execute normally.
                await session.rollback()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# ──────────────────────────────────────────────
# Synchronous Database Engine & Session Factory (for ported GitHub modules)
# ──────────────────────────────────────────────

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from collections.abc import Generator

_syncEngine: Engine | None = None
_syncSessionFactory: sessionmaker[Session] | None = None

def getSyncEngine() -> Engine:
    """Return the synchronous SQLAlchemy engine (created lazily on first call)."""
    global _syncEngine
    if _syncEngine is None:
        settings = getSettings()
        # Convert asyncpg connection string to standard postgresql if present
        url = settings.databaseUrl
        if url.startswith("postgresql+asyncpg://"):
            url = url.replace("postgresql+asyncpg://", "postgresql://", 1)
            if "ssl=require" in url:
                url = url.replace("ssl=require", "sslmode=require")
        elif url.startswith("sqlite+aiosqlite://"):
            url = url.replace("sqlite+aiosqlite://", "sqlite://", 1)

        kwargs = {
            "echo": settings.debug,
        }
        if url.startswith("sqlite"):
            from sqlalchemy.pool import StaticPool
            kwargs.update({
                "connect_args": {"check_same_thread": False},
                "poolclass": StaticPool,
            })
        else:
            kwargs.update({
                "pool_pre_ping": True,
                "pool_size": settings.dbPoolSize,
                "max_overflow": settings.dbMaxOverflow,
                "pool_timeout": settings.dbPoolTimeout,
                "pool_recycle": settings.dbPoolRecycle,
            })

        _syncEngine = create_engine(url, **kwargs)
    return _syncEngine

def getSyncSessionFactory() -> sessionmaker[Session]:
    """Return the synchronous session factory (created lazily on first call)."""
    global _syncSessionFactory
    if _syncSessionFactory is None:
        _syncSessionFactory = sessionmaker(
            bind=getSyncEngine(),
            autocommit=False,
            autoflush=False,
        )
    return _syncSessionFactory

def getSyncDb() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a synchronous database session.
    """
    sessionFactory = getSyncSessionFactory()
    db = sessionFactory()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()