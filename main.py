from fastapi import FastAPI
from app.lifespan import app_lifespan
from app.interfaces.middleware import add_middlewares
from app.interfaces.controllers.oauth2_controller import router as google_oauth2_router
from app.interfaces.controllers.test_controller import router as test_router 

# Create the FastAPI instance
app = FastAPI(
    title="Delphi",
    description="OAuth2 Integration with FastAPI",
    version="1.0.0",
    lifespan=app_lifespan,
)

# Add middlewares
add_middlewares(app)

# Include routes
app.include_router(google_oauth2_router)
app.include_router(test_router)
