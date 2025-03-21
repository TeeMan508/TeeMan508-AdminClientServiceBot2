from django.db import IntegrityError
from starlette.exceptions import HTTPException

from ..models import Client


def register_client_(client_id: str, complaint: str):
    try:
        Client.objects.create(tg_id=client_id, complaint=complaint)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Client already exists")