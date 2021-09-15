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
            "email": "a@mail.com",
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

    def test_login_valid_user(self):
        User.objects.create_user(**self.valid_payload)
        response = client.post(
            reverse("rest_login"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_login_valid_user_returns_token(self):
        User.objects.create_user(**self.valid_payload)
        response = client.post(
            reverse("rest_login"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(True if "key" in response.json() else False , True)



