from uuid import uuid4
from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Dict, Literal, List, Union
import pytz



class InitialData(BaseModel):
    """
    This class represents a single conversation that does not include any messages yet.
    """
    chat_id: str
    bot_id: str
    conversation_start_time: datetime
    number_of_messages: int

    @model_validator(mode="before")
    @classmethod
    def create_conversation_start_time(cls, values):
        conversation_start_time = values["conversation_start_time"]
        if isinstance(conversation_start_time, str):
            values["conversation_start_time"] = datetime.fromisoformat(conversation_start_time)

        return values


class ChatData(InitialData):
    """
    This class represents a single conversation that includes at least a user and a genie message.
    """
    last_message_time: datetime
    conversation_duration_secs: int


class Message(BaseModel):
    bot_id: str
    chat_id: str
    message_id: str
    identity: Literal["user", "bot"]
    message_content: str
    timestamp: datetime

    @model_validator(mode="before")
    @classmethod
    def create_message_timestamp(cls, values):
        if isinstance(values, Dict):
            timestamp = values["timestamp"]
            values["timestamp"] = datetime.fromisoformat(timestamp)

            return values


class DataTableItem(BaseModel):
    chat_id: str
    bot_id: str
    conversation_start_time: datetime
    number_of_messages: int
    conversation_duration_secs: int
    engagement_level: Literal["low", "medium", "high", "very_high"]


class DashboardAllChatsResponse(BaseModel):
    dashboard_all_chats_item_list: List[DataTableItem]
    count_chats_with_message: int
    count_chats_without_message: int
    daily_distribution_of_chats: List

class DashboardMessagesResponse(BaseModel):
    chat_id: str
    messages: List[Message]