from uuid import uuid4

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram import F
from aiohttp import ClientSession, ClientResponseError

from .router import router
from ...logger import logger, correlation_id_ctx
from ...messages import ERROR_MESSAGE, REGISTER_ADMIN_MSG, NO_CLIENT_MSG
from ...urls import REGISTER_ADMIN_URL, SET_NEXT_CLIENT_TO_ADMIN_URL

class AdminState(StatesGroup):
    active = State()


@router.callback_query(F.data == "register_admin")
async def register_admin(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.message.from_user is None:
        return

    body = {
        "tg_id" : str(callback_query.message.chat.id),
    }

    uid = str(uuid4())
    correlation_id_ctx.set(uid)
    headers = {
        "X-CORRELATION-ID": uid
    }

    logger.info("Registering admin...")
    text = REGISTER_ADMIN_MSG
    async with ClientSession() as session:
        async with session.post(url=REGISTER_ADMIN_URL, data=body, headers=headers) as response:
            try:
                response.raise_for_status()
            except ClientResponseError as e:
                text = f"{ERROR_MESSAGE}: {e}"
                await callback_query.message.answer(text)
                return

    logger.info("Setting client to admin...")
    async with ClientSession() as session:
        async with session.post(url=SET_NEXT_CLIENT_TO_ADMIN_URL, data=body, headers=headers) as response:
            try:
                response.raise_for_status()
                complaint_dict = await response.json()
                text = complaint_dict['complaint']
            except ClientResponseError:
                text = f"{NO_CLIENT_MSG}"
                await callback_query.message.answer(text)
                await state.set_state(AdminState.active)
                return

    logger.info("Admin registered.")
    await state.set_state(AdminState.active)
    await callback_query.message.edit_text(text)
    try:
        await callback_query.message.edit_reply_markup(None)
    except TelegramBadRequest:
        ...

