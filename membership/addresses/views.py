from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from accounts.models import AccountModel
from .serializers import AddressSerializer
from .models import AddressModel


# Create your views here.
class AddressView(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = AddressModel.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def get(self, request, address_id=None):
        if address_id:
            return self.get_address_by_id(request, address_id)
        addresses = AddressModel.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_address_by_id(self, request, address_id):
        address = get_object_or_404(AddressModel, id=address_id)
        serializer = AddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Postman에서 PUT 요청 보낼 때, body에 다음과 같이 넣어주자
    {
        "user": 1,
        "street": "123 Updated Street",
        "city": "Updated City",
        "state": "Updated State",
        "postal_code": "12345",
        "country": "Updated Country"
    }
    """
    def put(self, request, address_id):
        address = get_object_or_404(AddressModel, id=address_id)
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, address_id):
        address = get_object_or_404(AddressModel, id=address_id)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
