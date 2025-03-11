from src.common.models import BaseModel
from django.db import models

class User(BaseModel):
    tg_id = models.CharField(max_length=255, default="blank_id")

class Client(User):
    is_handling = models.BooleanField(default=False)
    complaint = models.CharField(max_length=255)

class Admin(User):
    is_busy = models.BooleanField(default=False)
    current_client = models.OneToOneField(Client, null=True, blank=True, on_delete=models.SET_NULL)


