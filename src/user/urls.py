from django.urls import path
from .views import *

app_name = 'user'

urlpatterns = [
    path('register_client', RegisterClientView.as_view()),
    path('register_admin', RegisterAdminView.as_view()),
    path('handle_complaint', HandleComplaintView.as_view()),
    path('clear_client', ClearClientView.as_view()),
    path('free_admin', FreeAdminView.as_view()),
    path('get_current_client', GetCurrentClientView.as_view()),
]
