from starlette.exceptions import HTTPException

from ..selectors import get_admin_sr_


def get_admin_by_client(client_id: str):
    admin_qs = get_admin_sr_("current_client").filter(current_client__tg_id=client_id)
    admin = admin_qs.first()

    if not admin:
        raise HTTPException(status_code=409)

    return admin.current_client.tg_id

