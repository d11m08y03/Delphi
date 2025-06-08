from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict 

class Settings(BaseSettings):
    # General App Settings
    SERVER_URL: str = Field(...) 
    FRONTEND_REDIRECT_URL: str = Field(...)

    # JWT Settings
    JWT_SECRET_KEY: str = Field(...)
    JWT_ALGORITHM: str = Field(...)

    # OpenAI Configuration
    OPENAI_API_KEY: str = Field(...)

    # Salesforce Configuration
    SALESFORCE_TOKEN: str = Field(...)
    SALESFORCE_USERNAME: str = Field(...)
    SALESFORCE_PASSWORD: str = Field(...)
    SALESFORCE_ORG_ID: str = Field(...)
    SALESFORCE_ADMIN_PROFILE_ID: str = Field(...)
    SALESFORCE_ADMIN_PROFILE_NAME: str = Field(...)

    # Google OAuth2 Configuration
    GOOGLE_CLIENT_ID: str = Field(...)
    GOOGLE_CLIENT_SECRET: str = Field(...)

    # Gemini API Configuration
    GEMINI_API_KEY_1: str = Field(...) 
    GEMINI_API_KEY: str = Field(...)   

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8', 
        extra='ignore' # Optional: 'ignore' or 'forbid' unknown env vars
    )

try:
    settings = Settings() # type: ignore[call-arg]
except ValidationError as e:
    raise
