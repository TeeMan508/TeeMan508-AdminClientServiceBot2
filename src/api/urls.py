from django.urls import path

from .views import *

app_name = 'admin_client_service_api'

urlpatterns = [
    path("register_client", RegisterClientView.as_view()),
    path("register_admin", RegisterAdminView.as_view()),
    path("set_client_to_admin", SetClientToRandomAdminView.as_view()),
    path("free_admin", FreeAdminAndDeleteClientView.as_view()),
    path("get_current_client", GetCurrentClientView.as_view()),
    path("get_admin", GetAdminByClientView.as_view()),
    path("set_next_client", SetNextClientToAdminView.as_view()),

]
