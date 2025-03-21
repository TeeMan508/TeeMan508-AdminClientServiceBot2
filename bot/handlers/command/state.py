from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from .router import router


@router.message(Command(commands=["state"]))
async def handle_id_command(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    await message.answer(
        f"State:{await state.get_state()}\nChat Id: <b>{message.chat.id}</b>",
    )