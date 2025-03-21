from ..selectors import get_client_
from .get import get_random_free_admin


def set_client_to_random_admin(client_id: str):
    tarnished = get_random_free_admin()
    client = get_client_(tg_id=client_id)

    tarnished.is_busy = True
    tarnished.current_client = client
    tarnished.save()

    client.is_handling = True
    client.save()

    return tarnished.tg_id
