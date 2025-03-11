from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import F
from aiohttp import ClientSession

from bot.handlers.command.router import router
from .router import router
# from ...logger import logger
from aiogram.fsm.state import State, StatesGroup


REGISTER_ADMIN_URL = "http://web:8000/api/user/register_admin"


class AdminState(StatesGroup):
    free = State()
    busy = State()


@router.callback_query(F.data == "register_admin")
async def register_admin(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.message.from_user is None:
        return

    body = {
        "tg_id" : callback_query.message.chat.id,
    }

    async with ClientSession() as session:
        async with session.post(url=REGISTER_ADMIN_URL, data=body) as response:
            # logger.info(response.status)
            print(response.status)

    await state.set_state(AdminState.free)

    await callback_query.message.edit_text("Admin has been registered. Waiting for client...")
    try:
        await callback_query.message.edit_reply_markup(None)
    except TelegramBadRequest:
        ...

