import uuid

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import ClientSession, ClientResponseError

from .router import router
from ..callback.admin import AdminState
from ...bot import bot
from ...logger import logger, correlation_id_ctx
from ...messages import ERROR_MESSAGE, NEXT_CLIENT_TEXT, NEXT_CLIENT_BUTTON_TEXT

from ...urls import FREE_ADMIN_URL, GET_CURRENT_CLIENT_URL


@router.message(AdminState.active)
async def send_answer_to_client(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return
    uid = str(uuid.uuid4())
    correlation_id_ctx.set(uid)
    headers = {
        "X-CORRELATION-ID": uid
    }

    async with ClientSession() as session:
        async with session.get(url=GET_CURRENT_CLIENT_URL, data={"tg_id": message.chat.id}, headers=headers) as response:
            try:
                response.raise_for_status()
                data = await response.json()
                client_id = data["tg_id"]
            except ClientResponseError as e:
                text = f"{ERROR_MESSAGE}: {e}"
                await message.answer(text)
                return

    await bot.send_message(int(client_id), message.text)

    async with ClientSession() as session:
        async with session.post(url=FREE_ADMIN_URL, data={"tg_id": message.chat.id}, headers=headers) as response:
            try:
                response.raise_for_status()
            except ClientResponseError as e:
                text = f"{ERROR_MESSAGE}: {e}"
                await message.answer(text)
                return

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=NEXT_CLIENT_BUTTON_TEXT, callback_data="next_client"))
    await message.answer(NEXT_CLIENT_TEXT, reply_markup=builder.as_markup())


