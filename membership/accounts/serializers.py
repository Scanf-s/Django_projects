from rest_framework.serializers import ModelSerializer
from .models import AccountModel


class AccountSerializer(ModelSerializer):
    class Meta:
        model = AccountModel
        fields = '__all__'
