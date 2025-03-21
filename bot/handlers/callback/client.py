from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import F
from aiohttp import ClientSession

from bot.handlers.command.router import router
from .router import router
# from ...logger import logger
from aiogram.fsm.state import State, StatesGroup

from ...messages import TYPE_COMPLAINT_TEXT


class ClientState(StatesGroup):
    active = State()
    registered = State()


@router.callback_query(F.data == "register_client")
async def register_client(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.message.from_user is None:
        return

    await state.set_state(ClientState.active)
    await callback_query.message.edit_text(TYPE_COMPLAINT_TEXT)
    try:
        await callback_query.message.edit_reply_markup(None)
    except TelegramBadRequest:
        ...


    