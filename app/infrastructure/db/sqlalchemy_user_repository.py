from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select
from sqlalchemy import Integer, String

from app.domain.models.user import User
from app.domain.interfaces.user_repository import UserRepository
from app.infrastructure.db.base import Base

class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

def orm_to_domain(user_orm: UserORM) -> User:
    return User(
        id=user_orm.id,
        name=user_orm.name,
        email=user_orm.email,
        password_hash=user_orm.password_hash,
    )

def domain_to_orm(user: User) -> UserORM:
    return UserORM(
        id=user.id,
        name=user.name,
        email=user.email,
        password_hash=user.password_hash,
    )

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        user_orm = domain_to_orm(user)
        self.session.add(user_orm)
        await self.session.commit()
        await self.session.refresh(user_orm)
        return orm_to_domain(user_orm)

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(UserORM).where(UserORM.email == email))
        user_orm = result.scalar_one_or_none()
        if user_orm:
            return orm_to_domain(user_orm)
        return None

    async def update(self, user: User) -> User:
        result = await self.session.execute(select(UserORM).where(UserORM.id == user.id))
        user_orm = result.scalar_one_or_none()
        if not user_orm:
            raise ValueError("User not found")

        user_orm.name = user.name
        user_orm.email = user.email
        user_orm.password_hash = user.password_hash

        self.session.add(user_orm)
        await self.session.commit()
        await self.session.refresh(user_orm)
        return User(id=user_orm.id, name=user_orm.name, email=user_orm.email, password_hash=user_orm.password_hash)
