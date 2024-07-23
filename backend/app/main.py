import os

import init_db
from api.route_base import api_router
from core.config import IN_PROD, POPULATE_DUMMY_DATA, SESSION_MIDDLEWARE_SECRET
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from populate_db import populate_dummy_data
from starlette.middleware.sessions import SessionMiddleware

ROOT_ROUTE = os.getenv("ROOT_ROUTE", "")


def init_app():
    """Inits the application"""
    new_app = FastAPI(
        root_path=ROOT_ROUTE,
        docs_url=None if IN_PROD else "/docs",
        redoc_url=None if IN_PROD else "/redoc",
    )
    new_app.include_router(api_router)

    allowed_origins = os.getenv(
        "CORS_ORIGINS", "http://localhost:3000,http://localhost:8000"
    ).split(",")

    new_app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    new_app.add_middleware(SessionMiddleware, secret_key=SESSION_MIDDLEWARE_SECRET)

    return new_app


app = init_app()

if POPULATE_DUMMY_DATA:
    populate_dummy_data()
