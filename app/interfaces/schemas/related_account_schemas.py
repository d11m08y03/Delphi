from pydantic import BaseModel

class RelatedAccountRequest(BaseModel):
    code: str
    user_id: int

class RelatedAccountResponse(BaseModel):
    success: bool
    message: str | None = None
