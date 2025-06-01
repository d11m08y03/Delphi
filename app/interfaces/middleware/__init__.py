from fastapi import FastAPI
from app.interfaces.middleware.cors import add_cors_middleware

def add_middlewares(app: FastAPI):
    add_cors_middleware(app)
