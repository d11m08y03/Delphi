from dataclasses import dataclass


@dataclass
class RelatedAccount:
    id: int | None
    user_id: int  # Foreign key to User.id
    provider: str  # e.g., "google", "microsoft", "custom"
    account_email: str  # Email associated with the external account
    access_token: str | None  # Optional, for OAuth
    refresh_token: str | None  # Optional, for OAuth
