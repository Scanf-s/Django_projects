from rest_framework.serializers import ModelSerializer
from .models import AddressModel


class AddressSerializer(ModelSerializer):
    class Meta:
        model = AddressModel
        fields = '__all__'
