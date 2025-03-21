from django.db import IntegrityError
from starlette.exceptions import HTTPException

from ..models import Admin


def register_admin_(admin_id: str):
    try:
        Admin.objects.create(tg_id=admin_id)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Admin already exists")