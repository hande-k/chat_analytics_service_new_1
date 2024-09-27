from collections import defaultdict
from src.models.dasboard_models import ChatData, DataTableItem, DashboardAllChatsResponse, InitialData, Message
from typing import Dict, List
from datetime import datetime, timedelta
import json
import os

class GetAllChatsManager:
    """
    The GetAllChatsManager is responsible for pulling data based on bot_id from local json files.
    """

    def __init__(self, base_path: str, bot_id: str):
        self.base_path = base_path
        
        self.file_name_raw_messages= "raw_messages.json"
        self.file_name_chats_wo_messages= "chats_wo_messages.json"
        self.file_name_aggreageted_conversations= "aggregated_conversations.json"

        self.bot_id = bot_id

        self.messages = self._read_and_filter_messages_from_json()
        self.chats_wo_messages = self._read_and_filter_conversations_wo_messages_from_json()
        self.conversations = self._aggreagate_raw_messages_to_conversations(messages=self.messages)

    def _read_and_filter_messages_from_json(self) -> List[Message]:
        """
        Reads and filters data from the JSON file based on bot_id.
        """
        try:
            file_path = os.path.join(self.base_path, self.file_name_raw_messages)
            with open(file_path, "r") as file:
                messages = json.load(file)
                # Filter the conversations by bot_id
                return [Message(**message) for message in messages if message.get("bot_id") == self.bot_id]
        except FileNotFoundError:
            print(f"File not found. Please check the file path: {file_path}")
            return []
        except json.JSONDecodeError:
            print("Error decoding JSON. Please check the file format.")
            return []
        

    def _read_and_filter_conversations_wo_messages_from_json(self) -> List[InitialData]:
        """
        Reads and filters data from the JSON file based on bot_id.
        """
        try:
            file_path = os.path.join(self.base_path, self.file_name_chats_wo_messages)
            with open(file_path, "r") as file:
                chats = json.load(file)
                # Filter the conversations by bot_id
                chats_wo_messages = [InitialData(**chat) for chat in chats if chat.get("bot_id") == self.bot_id]
                print(f"Retrieved {len(chats_wo_messages)} from json file.")
                return chats_wo_messages
        except FileNotFoundError:
            print(f"File not found. Please check the file path: {file_path}")
            return []
        except json.JSONDecodeError:
            print("Error decoding JSON. Please check the file format.")
            return []

    def _aggreagate_raw_messages_to_conversations(self, messages: List[Message]) -> List[ChatData]:
        chat_id_to_messages = {} # dict holding the chat_ids as keys and the list of its messages as values
        for message in messages:
            chat_id = message.chat_id
            if chat_id in chat_id_to_messages:
                chat_id_to_messages[chat_id].append(message)
            else:
                chat_id_to_messages[chat_id] = [message]
        
        conversations = []
        for chat_id, messages in chat_id_to_messages.items():
            sorted_messages: List[Message] = sorted(messages, key=lambda message: message.timestamp)
            number_of_messages = len(messages)
            conversation_start_time = sorted_messages[0].timestamp
            last_message_time = sorted_messages[-1].timestamp
            conversation_duration_secs = (last_message_time - conversation_start_time).seconds
            conversation = ChatData(chat_id=chat_id, bot_id=messages[0].bot_id, number_of_messages=number_of_messages, conversation_start_time=conversation_start_time, last_message_time=last_message_time, conversation_duration_secs=conversation_duration_secs)
            conversations.append(conversation)
        return conversations

    def group_chats_by_conversation_start_time_days(self):
        """
        Groups the chats based on the day values of the conversation_start_time to visualize, filling in missing dates.
        """

        chats_w_messages: List[ChatData] = self.conversations
        chats_wo_messages: List[InitialData] = self.chats_wo_messages
        print(f"Got {len(chats_w_messages)} chats with messages and {len(chats_wo_messages)} chats without messages.")

        date_groups = defaultdict(lambda: {"chats_with_messages_count": 0, "chats_without_messages_count": 0})

        # Determine the earliest and latest dates from data
        earliest_date = datetime.today().date()
        for chat in chats_w_messages + chats_wo_messages:
            chat_date = chat.conversation_start_time.date()
            if chat_date < earliest_date:
                earliest_date = chat_date

        # Populate dates with actual data
        for chat in chats_w_messages:
            start_date = chat.conversation_start_time.date().isoformat()
            date_groups[start_date]["chats_with_messages_count"] += 1

        for chat in chats_wo_messages:
            start_date = chat.conversation_start_time.date().isoformat()
            date_groups[start_date]["chats_without_messages_count"] += 1

        # Fill in missing dates with zeros
        current_date = earliest_date
        today_date = datetime.today().date()
        while current_date <= today_date:
            date_iso = current_date.isoformat()
            if date_iso not in date_groups:
                date_groups[date_iso] = {"chats_with_messages_count": 0, "chats_without_messages_count": 0}
            current_date += timedelta(days=1)

        return [{"date": date, **counts} for date, counts in sorted(date_groups.items())]

    def extend_conversation_data(self) -> List[DataTableItem]:
        dashboard_all_chats_item_list = []

        for conversation_data in self.conversations:

            if conversation_data.number_of_messages < 4:
                engagement_level = "low"
            elif conversation_data.number_of_messages < 7:
                engagement_level = "medium"
            elif conversation_data.number_of_messages < 10:
                engagement_level = "high"
            else:
                engagement_level = "very_high"

            dashboard_conv_item = DataTableItem(
                **conversation_data.model_dump(),
                engagement_level=engagement_level,
            )
            dashboard_all_chats_item_list.append(dashboard_conv_item)

        return dashboard_all_chats_item_list
