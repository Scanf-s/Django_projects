from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from accounts.models import AccountModel
from .models import AddressModel


class AddressAPITestCase(APITestCase):
    def setUp(self):
        self.user = AccountModel.objects.create_user(username='testuser', password='testpassword')
        self.address = AddressModel.objects.create(user=self.user, street="123 Elm St", city="Gotham", state="NY",
                                                   postal_code="12345", country="USA")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

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
            'street': "555 Elm St",
        }
        response = self.client.put(url, data, format='json')
        self.address.refresh_from_db()
        self.assertNotEquals(self.address.street, "124 Elm St")

    def test_delete_address(self):
        url = reverse('address-detail', kwargs={'address_id': self.address.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AddressModel.objects.filter(pk=self.address.pk).exists())
