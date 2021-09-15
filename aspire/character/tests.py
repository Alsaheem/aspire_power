import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from .models import Character, Quote
from django.contrib.auth.models import User


# initialize the APIClient app
client = Client()


# Create your tests here.


class CharacterTestCase(TestCase):
    def setUp(self):
        pass

    # test that character list comes back from api endpoint
    # test get quotes related to character using character id
    # test that a user can favorite a character | /characters/{id}/favorites
    # test that a user can favorite a character and a quote vis the quote id /characters/{id}/quotes/{id}/favorites
    # test that we can get allthe users favorites

    def test_get_characters(self):
        response = client.get(reverse("characters"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_character_quotes(self):
        response = client.get(reverse("list_character_quotes", kwargs={"character_id": "5cd99d4bde30eff6ebccfe9e"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # def test_get_characters(self):
    #     response = client.get(reverse("characters", kwargs={"pk": self.rambo.pk}))
    #     user = User.objects.get(pk=self.rambo.pk)
    #     serializer = UserSerializer(user)
    #     self.assertEqual(response.data, serializer.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
