from django.urls import path, include

# from .views import ProcessedImageView, UnprocessedImageView
app_name = 'admin_client_service_api'

urlpatterns = [
    path("user/", include(("src.user.urls", "user")))
]
