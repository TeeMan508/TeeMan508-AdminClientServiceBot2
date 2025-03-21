from starlette.exceptions import HTTPException

from ..models import Admin


def get_admin_(order_by=None, **filters):
    if order_by:
        admin_qs = Admin.objects.filter(**filters).order_by(*order_by)
    else:
        admin_qs = Admin.objects.filter(**filters)

    admin: Admin = admin_qs.first()
    if not admin:
        raise HTTPException(status_code=409)

    return admin
