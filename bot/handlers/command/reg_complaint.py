from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message
from aiohttp import ClientSession

from .router import router
from ..callback.admin import AdminState
from ..callback.client import ClientState

from ...bot import bot, dispatcher
from ...logger import logger

REGISTER_CLIENT_URL = "http://web:8000/api/user/register_client"
HANDLE_COMPLAINT_URL = "http://web:8000/api/user/handle_complaint"


@router.message(ClientState.register)
async def register_client_and_send_complaint(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    await message.answer("Wait for admin to handle your complaint")
    await state.set_state(ClientState.waiting)

    complaint = message.text
    client_id = message.chat.id
    #
    body = {
        "complaint" : complaint,
        "tg_id": client_id,
    }

    async with ClientSession() as session:
        async with session.post(url=REGISTER_CLIENT_URL, data=body) as response:
            logger.info(f"Register client. Status: {response.status}.")

        async with session.post(url=HANDLE_COMPLAINT_URL, data=body) as response:
            if response.status == 204:
                logger.info(f"Handle complaint request. Status: {response.status}. No free admins.")
                return

            if response.status == 400:
                logger.info(f"Handle complaint request. Status: {response.status}. Bad telegram id.")
                return

            if response.status == 200:
                logger.info(f"Handle complaint request. Status: {response.status}. OK")

            data = await response.json()
            await bot.send_message(data["tg_id"], data["complaint"])

            admin_state = FSMContext(storage=dispatcher.storage,
                                     key=StorageKey(
                                         chat_id=int(data["tg_id"]),
                                         user_id=int(data["tg_id"]),
                                         bot_id=bot.id
                                     ))
            await admin_state.set_state(AdminState.busy)


async def add_client_to_db_() -> None:

    body = {
        "complaint" : "complaint_123",
        "tg_id": 475403161,
    }

    async with ClientSession() as session:
        async with session.post(url=HANDLE_COMPLAINT_URL, data=body) as response:
            data = await response.json()
            try:
                await bot.send_message(data["tg_id"], data["complaint"])
            except TelegramBadRequest as e:
                print(f"{e}")
