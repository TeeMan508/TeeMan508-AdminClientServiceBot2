from aiogram.filters import Command
from aiogram.types import Message
from .router import router


@router.message(Command(commands=["id"]))
async def handle_id_command(message: Message) -> None:
    if message.from_user is None:
        return

    await message.answer(
        f"User Id: <b>{message.from_user.id}</b>\nChat Id: <b>{message.chat.id}</b>",
    )