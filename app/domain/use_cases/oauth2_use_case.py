from app.domain.models.user import User
from app.domain.models.related_account import RelatedAccount
from app.domain.interfaces.user_repository import UserRepository
from app.domain.interfaces.related_account_repository import RelatedAccountRepository


class OAuth2UserUseCase:
    def __init__(
        self, user_repo: UserRepository, related_account_repo: RelatedAccountRepository
    ):
        self.user_repo = user_repo
        self.related_account_repo = related_account_repo

    async def create_or_update_user(
        self,
        oauth_user: User,
        provider: str,
        account_email: str,
        access_token: str | None = None,
        refresh_token: str | None = None,
    ) -> User:
        existing_user = await self.user_repo.get_by_email(oauth_user.email)

        if existing_user and existing_user.id:
            updated = False
            if existing_user.name != oauth_user.name:
                existing_user.name = oauth_user.name
                updated = True

            if updated:
                await self.user_repo.update(existing_user)

            await self._upsert_related_account(
                user_id=existing_user.id,
                provider=provider,
                account_email=account_email,
                access_token=access_token or "",
                refresh_token=refresh_token,
            )

            return existing_user

        new_user = await self.user_repo.create(oauth_user)

        if not new_user.id:
            raise ValueError("Created user has no ID assigned")

        await self._upsert_related_account(
            user_id=new_user.id,
            provider=provider,
            account_email=account_email,
            access_token=access_token or "",
            refresh_token=refresh_token,
        )

        return new_user

    async def add_related_account(
        self,
        user_id: int,
        provider: str,
        account_email: str,
        access_token: str,
        refresh_token: str | None = None,
    ):
        await self._upsert_related_account(
            user_id=user_id,
            provider=provider,
            account_email=account_email,
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def _upsert_related_account(
        self,
        user_id: int,
        provider: str,
        account_email: str,
        access_token: str,
        refresh_token: str | None,
    ):
        existing_account = await self.related_account_repo.get_by_user_id_and_provider(
            user_id=user_id, provider=provider
        )

        if existing_account:
            changed = False
            if existing_account.account_email != account_email:
                existing_account.account_email = account_email
                changed = True

            if access_token and existing_account.access_token != access_token:
                existing_account.access_token = access_token
                changed = True

            if refresh_token and existing_account.refresh_token != refresh_token:
                existing_account.refresh_token = refresh_token
                changed = True

            if changed:
                await self.related_account_repo.update(existing_account)
        else:
            related_account = RelatedAccount(
                id=None,
                user_id=user_id,
                provider=provider,
                account_email=account_email,
                access_token=access_token,
                refresh_token=refresh_token,
            )
            await self.related_account_repo.create(related_account)
