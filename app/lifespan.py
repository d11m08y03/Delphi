from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.db.base import Base
from app.infrastructure.db.session import engine


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
