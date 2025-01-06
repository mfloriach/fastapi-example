from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from .config import env_vars

DATABASE_DSN = f"postgresql+asyncpg://{env_vars.DB_USER}:{env_vars.DB_PASS}@{env_vars.DB_HOST}:5432/{env_vars.DB_NAME}"

async_engine = create_async_engine(DATABASE_DSN, echo=True, future=True)

async def create_db_and_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
       bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
       yield session