import unittest
import json
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate, APIClient

from accounts.models import BarkeeperUser
from api.models import *
# Create your tests here.
class CocktailsTest(APITestCase):

    def test_post_cocktail(self):
        """ Ensure we can create a new cocktail object."""

        user = BarkeeperUser.objects.create_user(username='scivarolo')
        self.client.force_authenticate(user=user)

        cocktail = {
            "name": "Test Cocktail",
            "instructions": "Instructions",
            "notes": "Hey",
            "created_by": 1,
            "ingredients": [
                {
                    "ingredient": {
                        "name": "Gin",
                    },
                    "sort_order": 1,
                    "amount": 1.25,
                    "unit": "oz",
                    "created_by": 1
                },
                {
                    "ingredient": {
                        "name": "Green Chartreuse",
                    },
                    "sort_order": 2,
                    "amount": 1.25,
                    "unit": "oz",
                    "created_by": 1
                },
            ]
        }

        post_response = self.client.post('/api/cocktails/', cocktail, format='json')
        # check for item in database, and check that it is in the post response
        self.assertEqual(Cocktail.objects.count(), 1)
        self.assertContains(post_response, "Test Cocktail", status_code=201)
