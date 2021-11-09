import json

from django.conf import settings
from django.test import TestCase, Client


class PlayersTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.name = "read madrid"
        self.country = "spain"
        self.balance = settings.TEAM["initial_balance"]
        self.register()
        self.session = self.login()

    def register(self):
        register_data = {
            "email": "login@gmail.com",
            "password": "abc123",
            "repeated_password": "abc123",
            "team_name": self.name,
            "team_country": self.country,
        }
        self.client.post(
            path="/api/register",
            data=json.dumps(register_data),
            content_type='application/json'
        )

    def login(self):
        data = {
            "email": "login@gmail.com",
            "password": "abc123",
        }
        response = self.client.post(
            path="/api/login",
            data=json.dumps(data),
            content_type='application/json'
        )
        return json.loads(response.content)["session_id"]

    def test_team(self):
        response = self.client.get(
            path="/api/players",
            **{"HTTP_SESSION": self.session}
        )
        data = json.loads(response.content)
        number_of_players = \
            settings.TEAM["initial_goal_keepers"] + \
            settings.TEAM["initial_defenders"] + \
            settings.TEAM["initial_mid_fielders"] + \
            settings.TEAM["initial_attackers"]
        self.assertEqual(len(data), number_of_players)
        fields = ['identifier', 'first_name', 'last_name', 'country', 'age', 'market_value']
        for field in fields:
            self.assertTrue(field in data[0])
