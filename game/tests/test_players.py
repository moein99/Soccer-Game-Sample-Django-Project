import json

from django.conf import settings
from django.test import TestCase, Client
from rest_framework import status

from game.models import User, Player
from game.tests import TestMixin, Method, APIPath


class PlayersTestCase(TestCase, TestMixin):
    def setUp(self) -> None:
        self.client = Client()
        self.email1 = "email1@gmail.com"
        self.email2 = "email2@gmail.com"
        self.balance = settings.TEAM["initial_balance"]
        self.create_user(email=self.email1, password="abc123")
        self.create_user(email=self.email2, password="abc123")
        self.session1 = self.login(client=self.client, email=self.email1, password="abc123")
        self.session2 = self.login(client=self.client, email=self.email2, password="abc123")

    def call(self, method, session, data=None):
        if method == Method.get:
            return self.client.get(
                path=APIPath.players,
                **{"HTTP_SESSION": session}
            )
        elif method == Method.put:
            return self.client.put(
                path=f"{APIPath.players}/{data['identifier']}",
                data=json.dumps(data),
                content_type='application/json',
                **{"HTTP_SESSION": session}
            )

    def test_get_players(self):
        response = self.call(Method.get, self.session1)
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
        player_identifier = Player.objects.filter(team=user1.team)[0].identifier
        data = {
            "identifier": player_identifier,
            "first_name": "new name",
            "last_name": "new last name",
            "country": "new country",
        }
        response = self.call(Method.put, self.session1, data)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        update_fields = ['first_name', 'last_name', 'country']
        for field in update_fields:
            self.assertTrue(field in data)
        self.assertEqual(len(update_fields), len(data))
        player = Player.objects.get(identifier=player_identifier)
        self.assertEqual(player.first_name, "new name")
        self.assertEqual(player.last_name, "new last name")
        self.assertEqual(player.country, "new country")

    def test_403_when_trying_to_update_another_player(self):
        user1 = User.objects.get(email=self.email1)
        player_identifier = Player.objects.filter(team=user1.team)[0].identifier
        data = {
            "identifier": player_identifier,
            "first_name": "new name",
            "last_name": "new last name",
            "country_name": "new country",
        }
        response = self.call(Method.put, self.session2, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
