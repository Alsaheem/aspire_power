import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from .serializers import RegisterSerializer
from django.contrib.auth.models import User


# initialize the APIClient app
client = Client()


class RegisterUserTest(TestCase):
    """Test module for inserting a new user"""

    def setUp(self):
        self.valid_payload = {
            "username": "Muffin",
            "email": "",
            "password": "Pamerion",
        }
        self.invalid_payload = {
            "username": "",
            "email": "",
            "password": "Pamerion",
        }

    def test_create_valid_user(self):
        response = client.post(
            reverse("register"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        response = client.post(
            reverse("register"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class GetSingleUserTest(TestCase):
#     """Test module for GET single user API"""

#     def setUp(self):
#         self.casper = User.objects.create(
#             username="Casper", password="Bull Dog", email="Black@gmail.com"
#         )
#         self.muffin = User.objects.create(
#             username="Muffin", password="Gradane", email="Brown@gmail.com"
#         )
#         self.rambo = User.objects.create(
#             username="Rambo", password="Labrador", email="Black@gmail.com"
#         )
#         self.ricky = User.objects.create(
#             username="Ricky", password="Labrador", email="Brown@gmail.com"
#         )

#     def test_get_valid_single_user(self):
#         response = client.get(reverse("single_user", kwargs={"pk": self.rambo.pk}))
#         user = User.objects.get(pk=self.rambo.pk)
#         serializer = UserSerializer(user)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_get_invalid_single_user(self):
#         response = client.get(reverse("single_user", kwargs={"pk": 30}))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
