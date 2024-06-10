from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from accounts.models import AccountModel
from .models import AddressModel
from rest_framework_simplejwt.tokens import RefreshToken


class AddressAPITestCase(APITestCase):
    def setUp(self):
        self.user = AccountModel.objects.create_user(username='testuser', password='testpassword')
        self.address = AddressModel.objects.create(user=self.user, street="123 Elm St", city="Gotham", state="NY",
                                                   postal_code="12345", country="USA")

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_get_addresses_unauthorized(self):
        self.client.logout()
        url = reverse('address-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_addresses(self):
        url = reverse('address-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['street'], "123 Elm St")

    def test_create_address(self):
        url = reverse('address-list')
        data = {
            'user': self.user.id,
            'street': "124 Elm St",
            'city': "Gotham",
            'state': "NY",
            'postal_code': "12346",
            'country': "USA"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_address(self):
        url = reverse('address-detail', kwargs={'address_id': self.address.pk})
        data = {
            'city' : "new city",
            'street': "new street",
            'state': "new state",
            'postal_code': "new postal code",
            "country": "new country",
            "user": f"{self.user.pk}"
        }
        response = self.client.put(url, data, format='json')
        print("Response status:", response.status_code)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.address.refresh_from_db()
        self.assertEqual(self.address.street, "new street")

    def test_delete_address(self):
        url = reverse('address-detail', kwargs={'address_id': self.address.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AddressModel.objects.filter(pk=self.address.pk).exists())
