import json
from collections import Counter

from django.conf import settings
from django.test import TestCase, Client
from rest_framework import status

from game.models import Team, User, PlayerRole
from game.tests import APIPath


class RegisterTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def call(self, data):
        return self.client.post(
            path=APIPath.register,
            data=json.dumps(data),
            content_type='application/json'
        )

    def test_register(self):
        data = {
            "email": "abc@gmail.com",
            "password": "abc123",
            "repeated_password": "abc123",
            "team_name": "Real Madrid",
            "team_country": "Spain",
        }
        response = self.call(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Team.objects.count(), 1)
        number_of_players = \
            settings.TEAM["initial_goal_keepers"] + \
            settings.TEAM["initial_defenders"] + \
            settings.TEAM["initial_mid_fielders"] + \
            settings.TEAM["initial_attackers"]
        user = User.objects.all()[0]
        self.assertEqual(user.team.player_set.count(), number_of_players)
        self.assertEqual(user.team.balance, settings.TEAM["initial_balance"])
        self.assertEqual(user.team.value, settings.PLAYER["initial_market_value"] * number_of_players)
        roles_to_count = Counter(user.team.player_set.all().values_list("role", flat=True))
        self.assertEqual(roles_to_count[PlayerRole.ATTACKER], settings.TEAM["initial_attackers"])
        self.assertEqual(roles_to_count[PlayerRole.DEFENDER], settings.TEAM["initial_defenders"])
        self.assertEqual(roles_to_count[PlayerRole.MID_FIELDER], settings.TEAM["initial_mid_fielders"])
        self.assertEqual(roles_to_count[PlayerRole.GOAL_KEEPER], settings.TEAM["initial_goal_keepers"])

    def test_register_with_bad_inputs(self):
        bad_inputs = [
            {  # passwords do not match
                "email": "abc@gmail.com",
                "password": "abc123",
                "repeated_password": "abc122",
                "team_name": "Real Madrid",
                "team_country": "Spain",
            },
            {  # a field is missing
                "email": "abc@gmail.com",
                "repeated_password": "abc123",
                "team_name": "Real Madrid",
                "team_country": "Spain",
            },
            {  # a field is missing
                "email": "abc@gmail.com",
                "password": "abc123",
                "repeated_password": "abc123",
                "team_name": "Real Madrid",
            },
            {  # bad email format
                "email": "abc.gmail.com",
                "password": "abc123",
                "repeated_password": "abc123",
                "team_name": "Real Madrid",
            },
        ]
        for data in bad_inputs:
            response = self.call(data=data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
