from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from accounts.models import AccountModel
from .serializers import AddressSerializer
from .models import AddressModel


# Create your views here.
class AddressView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = AddressModel.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

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
        try:
            address = AddressModel.objects.get(id=address_id)
        except AddressModel.DoesNotExist:
            return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, address_id):
        try:
            address = AddressModel.objects.get(id=address_id)
        except AddressModel.DoesNotExist:
            return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
