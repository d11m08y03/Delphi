from pydantic import BaseModel


class OAuth2LoginResponse(BaseModel):
    redirect_url: str
