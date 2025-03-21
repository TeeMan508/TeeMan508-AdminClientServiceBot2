from starlette.exceptions import HTTPException

from ..logger import logger
from ..selectors import get_admin_, get_client_
from .get import get_unhandled_client

def set_next_client_to_admin(admin_id: str) -> str:
    admin = get_admin_(tg_id=admin_id)
    client = get_unhandled_client()

    if admin.is_busy:
        raise HTTPException(status_code=409, detail="Admin is busy")

    client.is_handling = True
    client.save()

    admin.is_busy = True
    admin.current_client = client
    admin.save()

    return client.complaint



