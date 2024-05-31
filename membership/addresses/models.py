from django.db import models
from common.models import CommonModel
from accounts.models import AccountModel


class AddressModel(CommonModel):
    user = models.ForeignKey(AccountModel, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user}'s address"
