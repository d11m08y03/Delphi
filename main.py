from fastapi import FastAPI

from app.interfaces.controllers.oauth2_controller import router as google_oauth2_router
from app.interfaces.controllers.test_controller import router as test_router
from app.interfaces.middleware import add_middlewares
from app.lifespan import app_lifespan

app = FastAPI(
    lifespan=app_lifespan,
)

add_middlewares(app)

app.include_router(google_oauth2_router)
app.include_router(test_router)
