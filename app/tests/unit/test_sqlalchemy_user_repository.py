import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.infrastructure.db.sqlalchemy_user_repository import SQLAlchemyUserRepository, UserORM
from app.infrastructure.db.base import Base
from app.domain.models.user import User

DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionTest = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created:", Base.metadata.tables.keys())
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def session():
    async with AsyncSessionTest() as session:
        yield session
        await session.rollback()

@pytest.mark.asyncio
async def test_create_user(session: AsyncSession):
    repo = SQLAlchemyUserRepository(session)
    user = User(id=None, name="Alice", email="alice@example.com", password_hash="hashedpwd")
    created_user = await repo.create(user)

    assert created_user.id is not None
    assert created_user.name == "Alice"
    assert created_user.email == "alice@example.com"

@pytest.mark.asyncio
async def test_get_by_email(session: AsyncSession):
    repo = SQLAlchemyUserRepository(session)
    user = UserORM(name="Bob", email="bob@example.com", password_hash="hashedpwd")

    session.add(user)
    await session.commit()

    fetched_user = await repo.get_by_email("bob@example.com")

    assert fetched_user is not None
    assert fetched_user.email == "bob@example.com"
    assert fetched_user.name == "Bob"

    missing_user = await repo.get_by_email("missing@example.com")

    assert missing_user is None
