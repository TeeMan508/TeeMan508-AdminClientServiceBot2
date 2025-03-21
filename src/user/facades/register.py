from ..interactors import register_client_, register_admin_
from ..schemas import ClientCredentials, AdminCredentials


def register_admin(creds: AdminCredentials):
    return register_admin_(creds.tg_id)

def register_client(creds: ClientCredentials):
    return register_client_(creds.tg_id, creds.complaint)