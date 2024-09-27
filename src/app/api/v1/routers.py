from fastapi import APIRouter

from src.app.api.v1.endpoints import get_detailed_messages
from src.app.api.v1.endpoints import get_all_chats

api_router = APIRouter()

api_router.include_router(get_all_chats.router, prefix="", tags=["initial_endpoints"])
api_router.include_router(get_detailed_messages.router, prefix="", tags=["initial_endpoints"])

