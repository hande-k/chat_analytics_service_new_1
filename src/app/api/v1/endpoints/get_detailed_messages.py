from datetime import datetime

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request
from typing import List

from pydantic import BaseModel
from src.models.dasboard_models import DashboardMessagesResponse, Message

from src.services.get_detailed_messages_manager import GetDetailedMessagesManager

load_dotenv()

router = APIRouter()


class GetMessagesRequest(BaseModel):
    chat_id: str

@router.post("/get-detailed-messages", response_model=DashboardMessagesResponse)
async def get_detailed_messages(get_messages_request: GetMessagesRequest):

    chat_id = get_messages_request.chat_id
    get_messages_manager = GetDetailedMessagesManager(base_path="src/data", chat_id=chat_id)
    chat_details_list = get_messages_manager.chat_details_list
    print(chat_details_list)
    messages = []

    for message_object in chat_details_list:
        chat_id = message_object["chat_id"]
        message = Message(
            message_id=message_object["message_id"],
            identity=message_object["identity"],
            message_content=message_object["message_content"],
            timestamp=message_object["timestamp"],
        )
        messages.append(message)

    try:
        chat_details_response = DashboardMessagesResponse(
            chat_id=chat_id,
            messages=messages,
        )
    except KeyError as e:
        raise HTTPException(status_code=500, detail="Internal Server Error: Data formatting error")

    return chat_details_response
