from typing import Dict, List
import json
import os

class GetDetailedMessagesManager:
    """
    The GetDetailedMessagesManager is responsible for pulling chat details data based on chat_id from the json file.
    """

    def __init__(self, base_path: str, chat_id: str):
        self.base_path = base_path

        self.file_name = "raw_messages.json"

        self.chat_id = chat_id
        
        self.chat_details_list = self.read_data_from_json()
    
    def read_data_from_json(self) -> List[Dict]:
        """
        Reads and filters data from the JSON file based on chat_id.
        """
        try:
            file_path = os.path.join(self.base_path, self.file_name)
            with open(file_path, "r") as file:
                data = json.load(file)
                # Filter the conversations by chat_id
                return [chat for chat in data if chat.get("chat_id") == self.chat_id]
        except FileNotFoundError:
            print("File not found. Please check the file path.")
            return []
        except json.JSONDecodeError:
            print("Error decoding JSON. Please check the file format.")
            return []
