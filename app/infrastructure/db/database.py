from app.infrastructure.db.session import engine
from app.infrastructure.db.base import Base 

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
