from starlette.exceptions import HTTPException

from src.user.logger import logger
from ..models import Client


def get_client_(order_by=None, **filters):
    if order_by:
        client_qs = Client.objects.filter(**filters).order_by(order_by)
    else:
        client_qs = Client.objects.filter(**filters)

    client: Client = client_qs.first()

    if not client:
        raise HTTPException(status_code=409)

    return client
