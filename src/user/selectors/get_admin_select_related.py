from django.db.models import QuerySet
from starlette.exceptions import HTTPException

from ..models import Admin


def get_admin_sr_(select_related="", **filters) -> QuerySet:
    admin_qs = Admin.objects.filter(**filters).select_related(select_related)

    admin: Admin = admin_qs.first()
    if not admin:
        raise HTTPException(status_code=409)

    return admin_qs
