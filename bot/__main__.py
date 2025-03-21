import asyncio
import logging.config
from .bot import _start_polling
from .logger import LOGGING_CONFIG


if __name__ == "__main__":
    logging.config.dictConfig(LOGGING_CONFIG)
    asyncio.run(_start_polling())