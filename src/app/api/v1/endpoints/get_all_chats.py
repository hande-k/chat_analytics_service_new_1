from fastapi import APIRouter

from src.models.dasboard_models import DashboardAllChatsResponse
from src.services.get_all_chats_manager import GetAllChatsManager
from config import DATA_DIR

router = APIRouter()


@router.get("/get-all-chats/", response_model=DashboardAllChatsResponse)
async def get_all_chats(bot_id: str):

    get_all_chats_manager = GetAllChatsManager(bot_id=bot_id, base_path=DATA_DIR)

    chats_with_messages_list = get_all_chats_manager.extend_conversation_data()
    chats_wo_messages = get_all_chats_manager.chats_wo_messages

    daily_distribution_of_chats = get_all_chats_manager.group_chats_by_conversation_start_time_days()

    all_chats_response = DashboardAllChatsResponse(
        dashboard_all_chats_item_list=chats_with_messages_list,
        count_chats_with_message=len(chats_with_messages_list),
        count_chats_without_message=len(chats_wo_messages),
        daily_distribution_of_chats=daily_distribution_of_chats,
    )
    return all_chats_response
