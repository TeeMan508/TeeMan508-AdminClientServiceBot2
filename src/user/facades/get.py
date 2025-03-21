from ..selectors import get_client_, get_admin_


def get_random_free_admin():
    return get_admin_(order_by='?', is_busy=False)

def get_unhandled_client():
    return get_client_(order_by="created_at", is_handling=False)

