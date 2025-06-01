from fastapi import FastAPI
from app.infrastructure.db.session import engine 
from app.infrastructure.db.base import Base
from typing import AsyncGenerator

async def app_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
