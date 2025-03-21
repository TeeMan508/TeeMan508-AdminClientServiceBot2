from starlette.exceptions import HTTPException

from ..selectors import get_admin_sr_

def get_current_client(admin_id: str) -> str:
    admin = get_admin_sr_("current_client", tg_id=admin_id).first()

    if not admin:
        raise HTTPException(status_code=409)

    if not admin.current_client:
        raise HTTPException(status_code=409)

    return admin.current_client.tg_id

