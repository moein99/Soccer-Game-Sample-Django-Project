import json

from django.test import TestCase, Client
from rest_framework import status

from game.models import User


class TeamTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.email = "login@gmail.com"
        self.register()
        self.session = self.login()

    def register(self):
        register_data = {
            "email": self.email,
            "password": "abc123",
            "repeated_password": "abc123",
            "team_name": "real madrid",
            "team_country": "spain",
        }
        self.client.post(
            path="/api/register",
            data=json.dumps(register_data),
            content_type='application/json'
        )

    def login(self):
        data = {
            "email": self.email,
            "password": "abc123",
        }
        response = self.client.post(
            path="/api/login",
            data=json.dumps(data),
            content_type='application/json'
        )
        return json.loads(response.content)["session_id"]

    def test_get_team(self):
        response = self.client.get(
            path="/api/team",
            **{"HTTP_SESSION": self.session}
        )
        data = json.loads(response.content)
        fields = ['name', 'country', 'balance', 'value']

        for field in fields:
            self.assertTrue(field in data)
        self.assertEqual(len(data), len(fields))

    def test_update_team(self):
        data = {
            "name": "New Real Madrid",
            "country": "USA",
        }
        response = self.client.post(
            path="/api/team",
            data=json.dumps(data),
            content_type='application/json',
            **{"HTTP_SESSION": self.session}
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        update_fields = ['name', 'country']
        for field in update_fields:
            self.assertTrue(field in data)
        team = User.objects.get(email=self.email).team
        self.assertEqual(team.name, "New Real Madrid")
        self.assertEqual(team.country, "USA")

