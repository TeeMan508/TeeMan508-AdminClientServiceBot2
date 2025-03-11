import uuid

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message
from aiohttp import ClientSession

from .router import router
from ..callback.admin import AdminState
from ...bot import bot, dispatcher
from ...logger import logger

CLEAR_CLIENT_URL = "http://web:8000/api/user/clear_client"
FREE_ADMIN_URL = "http://web:8000/api/user/free_admin"
GET_CURRENT_CLIENT = "http://web:8000/api/user/get_current_client"


@router.message(AdminState.busy)
async def send_answer_to_client(message: Message, state: FSMContext) -> None:

    if message.from_user is None:
        return

    async with ClientSession() as session:
        async with session.post(url=GET_CURRENT_CLIENT, data={"tg_id": message.chat.id}) as response:
            if response.status == 204:
                logger.info(f"Get current client request. Status: {response.status}. Wrong telegram id.")
                return

            if response.status == 200:
                logger.info(f"FGet current client request. Status: {response.status}")

                data = await response.json()
                client_id = data["tg_id"]

    await bot.send_message(client_id, message.text) # ???

    async with ClientSession() as session:
        async with session.post(url=CLEAR_CLIENT_URL, data={"tg_id": client_id}) as response:
            if response.status == 200:
                logger.info(f"Clear client request. Status: {response.status}")

            if response.status == 204:
                logger.info(f"Clear client request. Status: {response.status}. Wrong telegram id.")

        await state.set_state(AdminState.free)

        client_state = FSMContext(storage=dispatcher.storage,
                                  key=StorageKey(
                                      chat_id=int(client_id),
                                      user_id=int(client_id),
                                      bot_id=bot.id
                                  ))
        await client_state.clear()

        uid = str(uuid.uuid4())
        from bot.logger import correlation_id_ctx
        correlation_id_ctx.set(uid)

        async with session.post(url=FREE_ADMIN_URL, data={"tg_id": message.chat.id}, headers={}) as response:
            if response.status == 200:
                logger.info(f"Free admin request. Status: {response.status}")
                data = await response.json()

                bot.send_message(data["tg_id"], data["complaint"])
                admin_state = FSMContext(storage=dispatcher.storage,
                                         key=StorageKey(
                                             chat_id=int(data["tg_id"]),
                                             user_id=int(data["tg_id"]),
                                             bot_id=bot.id
                                         ))

                await admin_state.set_state(AdminState.busy)


            if response.status == 204:
                logger.info(f"Free admin request. Status: {response.status}. Wrong telegram id.")

            if response.status == 207:
                logger.info(f"Free admin request. Status: {response.status}. No more clients.")


