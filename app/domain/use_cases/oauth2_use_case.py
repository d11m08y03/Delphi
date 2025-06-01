from app.domain.models.user import User
from app.domain.interfaces.user_repository import UserRepository

class OAuth2UserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_or_update_user(self, oauth_user: User) -> User:
        existing_user = await self.user_repo.get_by_email(oauth_user.email)
        if existing_user:
            updated = False
            if existing_user.name != oauth_user.name:
                existing_user.name = oauth_user.name
                updated = True

            if existing_user.password_hash != oauth_user.password_hash:
                existing_user.password_hash = oauth_user.password_hash
                updated = True

            if updated:
                return await self.user_repo.update(existing_user)  
            return existing_user

        return await self.user_repo.create(oauth_user)
