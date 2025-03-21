import logging.config
import sys
from enum import Enum

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config.settings.settings import settings

from bot.handlers.command.router import router as command_router
from bot.handlers.callback.router import router as callback_router
from .logger import logger, LOGGING_CONFIG


class RunningMode(str, Enum):
    LONG_POLLING = "LONG_POLLING"
    WEBHOOK = "WEBHOOK"


if not settings.BOT_TOKEN:
    logger.error("`TELEGRAM_API_TOKEN` is not set")
    sys.exit(1)

RUNNING_MODE = RunningMode.LONG_POLLING
print(settings.BOT_TOKEN)
bot = Bot(token=settings.BOT_TOKEN)

dispatcher = Dispatcher()
dispatcher.include_router(command_router)
dispatcher.include_router(callback_router)


async def set_bot_commands() -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="/start", description="Register the bot"),
            BotCommand(command="/id", description="Get the user and chat ids"),
            BotCommand(command="/state", description="Get the user and chat ids"),
        ],
    )


@dispatcher.startup()
async def on_startup() -> None:
    await set_bot_commands()


async def _start_polling() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)
    logger.info("Starting polling")

    await dispatcher.start_polling(bot, handle_signals=False, allowed_updates=["message", "edited_channel_post", "callback_query"])
