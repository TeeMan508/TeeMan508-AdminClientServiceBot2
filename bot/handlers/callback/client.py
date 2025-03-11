from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import F
from aiohttp import ClientSession

from bot.handlers.command.router import router
from .router import router
# from ...logger import logger
from aiogram.fsm.state import State, StatesGroup


class ClientState(StatesGroup):
    register = State()
    waiting = State()


@router.callback_query(F.data == "register_client")
async def register_client(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.message.from_user is None:
        return

    await state.set_state(ClientState.register)
    await callback_query.message.edit_text("Type your complaint:")
    try:
        await callback_query.message.edit_reply_markup(None)
    except TelegramBadRequest:
        ...


    