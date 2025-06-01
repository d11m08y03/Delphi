from pydantic import BaseModel

class OAuth2LoginResponse(BaseModel):
    auth_url: str

class OAuth2CallbackResponse(BaseModel):
    message: str
    user: dict
