# main.py
from fastapi import FastAPI

from .api.v1.routers import api_router

#### run with "poetry run uvicorn src.app.main:app --port 5001"
app = FastAPI(title="new-chat-analytics-service", version="0.0.1")

app.include_router(api_router, prefix="")
