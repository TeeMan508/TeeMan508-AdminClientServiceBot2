from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .router import router
from ...messages import REGISTER_TEXT


@router.message(Command("start"))
async def handle_start_command(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Client", callback_data="register_client"))
    builder.add(InlineKeyboardButton(text="Admin", callback_data="register_admin"))

    await message.answer(REGISTER_TEXT, reply_markup=builder.as_markup())



