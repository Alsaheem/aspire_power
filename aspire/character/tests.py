from django.test import TestCase
from django.contrib.auth.models import User


# Create your tests here.


class CharacterTestCase(TestCase):
    def setUp(self):
        pass

    # test that character list comes back from api endpoint
    # test get quotes related to character using character id
    # test that a user can favorite a character | /characters/{id}/favorites
    # test that a user can favorite a character and a quote vis the quote id /characters/{id}/quotes/{id}/favorites
    # test that we can get allthe users favorites
