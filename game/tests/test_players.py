import json

from django.conf import settings
from django.test import TestCase, Client
from rest_framework import status

from game.models import User, Ownership, Player


class PlayersTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.email1 = "email1@gmail.com"
        self.email2 = "email2@gmail.com"
        self.balance = settings.TEAM["initial_balance"]
        self.register(self.email1, "team1")
        self.register(self.email2, "team2")
        self.session1 = self.login(self.email1)
        self.session2 = self.login(self.email2)

    def register(self, email, team_name):
        register_data = {
            "email": email,
            "password": "abc123",
            "repeated_password": "abc123",
            "team_name": team_name,
            "team_country": "Spain",
        }
        self.client.post(
            path="/api/register",
            data=json.dumps(register_data),
            content_type='application/json'
        )

    def login(self, email):
        data = {
            "email": email,
            "password": "abc123",
        }
        response = self.client.post(
            path="/api/login",
            data=json.dumps(data),
            content_type='application/json'
        )
        return json.loads(response.content)["session_id"]

    def test_get_players(self):
        response = self.client.get(
            path="/api/players",
            **{"HTTP_SESSION": self.session1}
        )
        data = json.loads(response.content)
        number_of_players = \
            settings.TEAM["initial_goal_keepers"] + \
            settings.TEAM["initial_defenders"] + \
            settings.TEAM["initial_mid_fielders"] + \
            settings.TEAM["initial_attackers"]
        self.assertEqual(len(data), number_of_players)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fields = ['identifier', 'first_name', 'last_name', 'country', 'age', 'market_value']
        for field in fields:
            self.assertTrue(field in data[0])

    def test_update_player(self):
        user1 = User.objects.get(email=self.email1)
        player_identifier = Ownership.objects.filter(team=user1.team)[0].player.identifier
        data = {
            "identifier": player_identifier,
            "first_name": "new name",
            "last_name": "new last name",
            "country": "new country",
        }
        response = self.client.post(
            path="/api/players",
            data=json.dumps(data),
            content_type='application/json',
            **{"HTTP_SESSION": self.session1}
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        update_fields = ['identifier', 'first_name', 'last_name', 'country']
        for field in update_fields:
            self.assertTrue(field in data)
        self.assertEqual(len(update_fields), len(data))
        player = Player.objects.get(identifier=player_identifier)
        self.assertEqual(player.first_name, "new name")
        self.assertEqual(player.last_name, "new last name")
        self.assertEqual(player.country, "new country")

    def test_403_when_trying_to_update_another_player(self):
        user1 = User.objects.get(email=self.email1)
        player_identifier = Ownership.objects.filter(team=user1.team)[0].player.identifier
        data = {
            "identifier": player_identifier,
            "first_name": "new name",
            "last_name": "new last name",
            "country_name": "new country",
        }
        response = self.client.post(
            path="/api/players",
            data=json.dumps(data),
            content_type='application/json',
            **{"HTTP_SESSION": self.session2}  # another user tries to update the player
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
