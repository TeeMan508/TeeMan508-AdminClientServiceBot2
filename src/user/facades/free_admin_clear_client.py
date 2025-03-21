from ..selectors import get_admin_, get_admin_sr_
from ..schemas import AdminCredentials


def free_admin_and_clear_client(admin_creds: AdminCredentials):
    tarnished = get_admin_sr_(select_related="current_client", tg_id=admin_creds.tg_id).first()

    tarnished.is_busy = False
    tarnished.save()
    tarnished.current_client.delete()


