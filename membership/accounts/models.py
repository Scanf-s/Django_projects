from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import CommonModel
# Create your models here.


class AccountModel(AbstractUser, CommonModel):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
