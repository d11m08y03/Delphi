# Getting Started
## Local Environment Setup
1. Create and activate a virtual environment
	```sh
	python -m venv venv
	source venv/bin/activate
	```
2. Install dependencies
	```sh
    python -m venv venv
    source venv/bin/activate
	```
3. Run the development server
	```sh
	uvicorn main:app --reload
	```
## Docker Setup
Run the application using docker:
```sh
docker compose up
```
## Environment Variables
Below are the required environment variables. Ensure these are set in your `.env` file or environment configuration.
```sh
# General App Settings
SERVER_URL=
FRONTEND_REDIRECT_URL=

# JWT Settings
JWT_SECRET_KEY=
JWT_ALGORITHM=

# OpenAI Configuration
OPENAI_API_KEY=

# Salesforce Configuration
SALESFORCE_TOKEN=
SALESFORCE_USERNAME=
SALESFORCE_PASSWORD=
SALESFORCE_ORG_ID=
SALESFORCE_ADMIN_PROFILE_ID=
SALESFORCE_ADMIN_PROFILE_NAME=

# Google OAuth2 Configuration
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# Gemini API Configuration
GEMINI_API_KEY_1=
GEMINI_API_KEY=
```
