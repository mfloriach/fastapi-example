from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

DATABASE_DSN = "sqlite+aiosqlite:///:memory:"

async_engine = create_async_engine(DATABASE_DSN, connect_args={"check_same_thread": False}, poolclass=StaticPool)

async def override_get_session():
    async_session = sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )
    
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    async with async_session() as session:
       yield session
