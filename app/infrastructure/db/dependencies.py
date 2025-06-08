from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.interfaces.related_account_repository import RelatedAccountRepository
from app.infrastructure.db.session import get_session
from app.infrastructure.db.sqlalchemy_related_account_repository import (
    SQLAlchemyRelatedAccountRepository,
)
from app.infrastructure.db.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.domain.interfaces.user_repository import UserRepository


async def get_user_repository(
    db_session: AsyncSession = Depends(get_session),
) -> UserRepository:
    return SQLAlchemyUserRepository(session=db_session)


async def get_related_account_repository(
    db_session: AsyncSession = Depends(get_session),
) -> RelatedAccountRepository:
    return SQLAlchemyRelatedAccountRepository(session=db_session)
