from django.db.models import UniqueConstraint

from src.common.models import BaseModel
from django.db import models

class User(BaseModel):
    tg_id = models.CharField(max_length=255, default="blank_id", db_index=True)

    class Meta:
        abstract = True

class Client(User):
    is_handling = models.BooleanField(default=False)
    complaint = models.CharField(max_length=255)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['tg_id'], name="unique_client"  # noqa
            ),
        ]

class Admin(User):
    is_busy = models.BooleanField(default=False, db_index=True)
    current_client = models.OneToOneField(Client, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['tg_id'], name="unique_admin"  # noqa
            ),
        ]


