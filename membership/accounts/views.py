from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import AccountModel
from addresses.models import AddressModel
from addresses.serializers import AddressSerializer


# Create your views here.
class AccountView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(AccountModel, id=user_id)
        address = AddressModel.objects.filter(user=user)
        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data)

    def post(self, request, user_id):
        user = get_object_or_404(AccountModel, id=user_id)
        new_address = AddressModel.objects.create(
            user=user,
            city="API가 만들었어요",
            country="API가 만들었어요",
            street="API가 만들었어요",
            state="API가 만들었어요",
            postal_code="API가 만들었어요"
        )
        new_address.save()
        return Response(status=200)
