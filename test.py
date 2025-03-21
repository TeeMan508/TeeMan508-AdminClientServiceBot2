import asyncio

from bot.handlers.command.reg_complaint import add_client_to_db_

if __name__ == '__main__':
    asyncio.run(add_client_to_db_())