from fastapi import FastAPI
from app.interfaces.middleware.cors import add_cors_middleware
from app.interfaces.middleware.error_handling import ErrorHandlingMiddleware

def add_middlewares(app: FastAPI):
    add_cors_middleware(app)
    app.add_middleware(ErrorHandlingMiddleware)
