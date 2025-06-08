from typing import Optional

from sqlalchemy import ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.interfaces.related_account_repository import RelatedAccountRepository
from app.domain.models.related_account import RelatedAccount
from app.infrastructure.db.base import Base


class RelatedAccountORM(Base):
    __tablename__ = "related_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    provider: Mapped[str] = mapped_column(String, nullable=False)
    account_email: Mapped[str] = mapped_column(String, nullable=False)
    access_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    refresh_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    expires_at: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


def orm_to_domain(related_account_orm: RelatedAccountORM) -> RelatedAccount:
    return RelatedAccount(
        id=related_account_orm.id,
        user_id=related_account_orm.user_id,
        provider=related_account_orm.provider,
        account_email=related_account_orm.account_email,
        access_token=related_account_orm.access_token,
        refresh_token=related_account_orm.refresh_token,
    )


def domain_to_orm(related_account: RelatedAccount) -> RelatedAccountORM:
    return RelatedAccountORM(
        id=related_account.id,
        user_id=related_account.user_id,
        provider=related_account.provider,
        account_email=related_account.account_email,
        access_token=related_account.access_token,
        refresh_token=related_account.refresh_token,
    )


class SQLAlchemyRelatedAccountRepository(RelatedAccountRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, related_account: RelatedAccount) -> RelatedAccount:
        related_account_orm = domain_to_orm(related_account)

        self.session.add(related_account_orm)
        await self.session.commit()
        await self.session.refresh(related_account_orm)

        return orm_to_domain(related_account_orm)

    async def get_by_id(self, id: int) -> Optional[RelatedAccount]:
        result = await self.session.execute(
            select(RelatedAccountORM).where(RelatedAccountORM.id == id)
        )

        related_account_orm = result.scalar_one_or_none()
        if related_account_orm:
            return orm_to_domain(related_account_orm)

        return None

    async def get_by_user_id(self, user_id: int) -> list[RelatedAccount]:
        result = await self.session.execute(
            select(RelatedAccountORM).where(RelatedAccountORM.user_id == user_id)
        )

        related_accounts = result.scalars().all()

        return [orm_to_domain(acc) for acc in related_accounts]

    async def get_by_user_id_and_provider(
        self, user_id: int, provider: str
    ) -> Optional[RelatedAccount]:
        result = await self.session.execute(
            select(RelatedAccountORM).where(
                RelatedAccountORM.user_id == user_id,
                RelatedAccountORM.provider == provider,
            )
        )

        related_account_orm = result.scalar_one_or_none()
        if related_account_orm:
            return orm_to_domain(related_account_orm)

        return None

    async def update(self, related_account: RelatedAccount) -> RelatedAccount:
        result = await self.session.execute(
            select(RelatedAccountORM).where(RelatedAccountORM.id == related_account.id)
        )

        related_account_orm = result.scalar_one_or_none()
        if not related_account_orm:
            raise ValueError("Related account not found")

        related_account_orm.account_email = related_account.account_email
        related_account_orm.access_token = related_account.access_token
        related_account_orm.refresh_token = related_account.refresh_token

        self.session.add(related_account_orm)
        await self.session.commit()
        await self.session.refresh(related_account_orm)

        return orm_to_domain(related_account_orm)

    async def delete(self, id: int) -> None:
        result = await self.session.execute(
            select(RelatedAccountORM).where(RelatedAccountORM.id == id)
        )

        related_account_orm = result.scalar_one_or_none()
        if related_account_orm:
            await self.session.delete(related_account_orm)
            await self.session.commit()
