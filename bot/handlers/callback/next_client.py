from uuid import uuid4

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram import F
from aiohttp import ClientSession, ClientResponseError
from starlette.exceptions import HTTPException

from .router import router
from ...logger import logger, correlation_id_ctx
from ...messages import NO_CLIENT_MSG

from ...urls import SET_NEXT_CLIENT_TO_ADMIN_URL


@router.callback_query(F.data == "next_client")
async def get_next_client_complaint(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.message.from_user is None:
        return

    body = {
        "tg_id" : callback_query.message.chat.id,
    }
    uid = str(uuid4())
    correlation_id_ctx.set(uid)
    headers = {
        "X-CORRELATION-ID": uid
    }

    async with ClientSession() as session:
        async with session.post(url=SET_NEXT_CLIENT_TO_ADMIN_URL, data=body, headers=headers) as response:
            try:
                response.raise_for_status()
                response_data = await response.json()
                unhandled_client_complaint = response_data["complaint"]
            except ClientResponseError:
                await callback_query.message.answer(NO_CLIENT_MSG)
                return

    try:
        await callback_query.message.edit_reply_markup(None)
        await callback_query.answer(unhandled_client_complaint)
    except TelegramBadRequest:
        ...

