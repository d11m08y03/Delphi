import os
import pytest
from pydantic import ValidationError
from app.core.config import Settings

# Helper function to clear env vars used in Settings
def clear_env_vars():
    keys = [
        "SERVER_URL", "FRONTEND_REDIRECT_URL", "JWT_SECRET_KEY",
        "OPENAI_API_KEY", "SALESFORCE_TOKEN", "SALESFORCE_USERNAME",
        "SALESFORCE_PASSWORD", "SALESFORCE_ORG_ID", "SALESFORCE_ADMIN_PROFILE_ID",
        "SALESFORCE_ADMIN_PROFILE_NAME", "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET",
        "GEMINI_API_KEY_1", "GEMINI_API_KEY"
    ]

    for key in keys:
        os.environ.pop(key, None)

def test_settings_loads_with_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_env_vars()

    # Set dummy env vars
    monkeypatch.setenv("SERVER_URL", "http://localhost:5000")
    monkeypatch.setenv("FRONTEND_REDIRECT_URL", "http://frontend.local")
    monkeypatch.setenv("JWT_SECRET_KEY", "supersecret")
    monkeypatch.setenv("OPENAI_API_KEY", "openai-key")
    monkeypatch.setenv("SALESFORCE_TOKEN", "sf-token")
    monkeypatch.setenv("SALESFORCE_USERNAME", "sf-user")
    monkeypatch.setenv("SALESFORCE_PASSWORD", "sf-pass")
    monkeypatch.setenv("SALESFORCE_ORG_ID", "sf-org")
    monkeypatch.setenv("SALESFORCE_ADMIN_PROFILE_ID", "sf-admin-id")
    monkeypatch.setenv("SALESFORCE_ADMIN_PROFILE_NAME", "System Administrator")
    monkeypatch.setenv("GOOGLE_CLIENT_ID", "google-client-id")
    monkeypatch.setenv("GOOGLE_CLIENT_SECRET", "google-secret")
    monkeypatch.setenv("GEMINI_API_KEY_1", "gemini-key-1")
    monkeypatch.setenv("GEMINI_API_KEY", "gemini-key-2")

    settings = Settings() # type: ignore[call-arg]

    assert settings.SERVER_URL == "http://localhost:5000"
    assert settings.JWT_SECRET_KEY == "supersecret"
    assert settings.OPENAI_API_KEY == "openai-key"
    assert settings.SALESFORCE_USERNAME == "sf-user"
    assert settings.GOOGLE_CLIENT_ID == "google-client-id"
    assert settings.GEMINI_API_KEY == "gemini-key-2"
