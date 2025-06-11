from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from settings import Config

# Для асинхронного подключения используем asyncpg
async_database_url = Config.SQLALCHEMY_DATABASE_URI.replace('postgresql://', 'postgresql+asyncpg://')
async_engine = create_async_engine(
    async_database_url,
    echo=True
)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Для синхронного подключения используем psycopg2
sync_database_url = Config.SQLALCHEMY_DATABASE_URI.replace('postgresql://', 'postgresql+psycopg2://')
sync_engine = create_engine(sync_database_url, echo=True)
SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()


async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session


def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
