from datetime import datetime
from zoneinfo import ZoneInfo

from tortoise import fields, models


class User(models.Model):

    id = fields.IntField(pk=True)

    username = fields.CharField(max_length=120, min_lenght=4)
    email = fields.CharField(max_length=120, null=True, unique=False)
    password = fields.CharField(max_length=100)
    photo = fields.CharField(max_length=60, null=True)
    email_search_hash = fields.CharField(
        max_length=64, unique=True, db_index=True
    )
    status = fields.BooleanField(default=True)
    verified_account = fields.BooleanField(default=False)
    temporary_code = fields.CharField(max_length=10, null=True)
    created_in = fields.DatetimeField(
        auto_now_add=True,
    )
    updated_in = fields.DatetimeField(
        auto_now=True,
    )

    class Meta:   # type: ignore
        table = 'users'

    def __str__(self):
        return f'User: {self.email}'
