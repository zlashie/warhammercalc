### Dependencies
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Faction

### How to run tests
# python manage.py test

### Classes
class FactionAPITest(APITestCase):
    def setUp(self):
        self.faction = Faction.objects.create(name="Ultramarines")

    def test_factions_list(self):
        url = reverse('faction-list') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Ultramarines", str(response.data))

class BasicEndpointTests(APITestCase):
    def test_all_endpoints_return_200(self):
        endpoints = [
            'faction-list',
            'unit-list',
            'unitstats-list',
            'unittype-list',
            'keyword-list',
            'unitkeyword-list',
            'ability-list',
            'weapon-list',
            'weaponkeyword-list',
        ]
        for endpoint in endpoints:
            url = reverse(endpoint)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK, f"{endpoint} failed")