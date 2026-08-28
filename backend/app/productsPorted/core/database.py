# Owner - pradhansaikat123@gmail.com

# Asynchronous database connection setup. Initializes SQLAlchemy engine and session,
# and provides the get_db dependency injection generator for routers.

# Import AsyncSession, async_sessionmaker, and create_async_engine from sqlalchemy.ext.asyncio for database connectivity
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
# Import DeclarativeBase from sqlalchemy.orm to use as base class for models
from sqlalchemy.orm import DeclarativeBase

# Import settings to access configured variables like database URL
from app.productsPorted.core.config import settings

# For SQLite async engine, we might want to check the URL and customize the engine arguments (e.g. check_same_thread=False)
connectArgs = {}
if settings.databaseUrl.startswith("sqlite"):
    connectArgs["check_same_thread"] = False

engine = create_async_engine(
    settings.databaseUrl,
    echo=True,
    connect_args=connectArgs if connectArgs else {},
    pool_pre_ping=True,
    pool_recycle=30
)
asyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with asyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
