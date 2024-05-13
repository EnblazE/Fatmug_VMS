import json
import uuid

from django.contrib.auth import get_user_model
from django.urls import reverse, path, include
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, URLPatternsTestCase


class DefaultTestCase(APITestCase, URLPatternsTestCase):
    """
    This test class will test creating three types of models available in the project using drf
        - Vendor, Purchase_Order
    """
    urlpatterns = [
        path('api/', include("vms_api.urls"))
    ]

    def setUp(self) -> None:
        """
        Setting up required attributes for our test. Please customize as you needed
        :return: None
        """
        self.username = "admin"
        self.password = "admin"
        self.user = get_user_model().objects.create_user(username='admin', password='admin')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        # required fields for Vendor model
        self.name = "Winnifred Lydia"  # switch with your own
        self.contact_details = "Phone: (509) 702-6224, Email: w.lydia@metropolishidden.com"  # replace with your own
        self.address = "2084 Lowell Isle Serenityfort, TN 05148"  # replace with your own
        self.vendor_code = str(uuid.uuid4())  # a random 36 digit uuid string

    def test_vendor_api(self):
        vendor_url_list = reverse('vendors_api_endpoints-list')
        payload = {
            'name': self.name,
            'contact_details': self.contact_details,
            'address': self.address,
            'vendor_code': self.vendor_code
        }
        # first we are testing if the authentication via token is successful or not
        self.assertTrue(get_user_model().objects.get(username='admin').is_authenticated, "User is not authenticated")
        # we will create a dummy vendor object
        response = self.client.post(vendor_url_list, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # we will try to view the object from our previous operation via <Action Retrieve>
        vendor_url_detail = reverse('vendors_api_endpoints-detail', kwargs={'pk': 1})
        response = self.client.get(vendor_url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # now we will try to update one of it's fields and check if it works
        updated_payload = {
            "address": "2789 Terrwood Dr E #21 Macungie, Pennsylvania(PA), 18062"
        }
        response = self.client.patch(vendor_url_detail, updated_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the partial update was successful or not
        response = self.client.get(vendor_url_detail, format='json')
        # the response.content is byte data, hence we need to parse it to json
        self.assertEqual(json.loads(response.content)["address"], updated_payload["address"])
