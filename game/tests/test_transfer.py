import json

from django.test import TestCase, Client
from rest_framework import status

from game.models import User, Player, Transfer
from game.tests import TestMixin, Method, APIPath


class TransferTestCase(TestCase, TestMixin):
    def setUp(self) -> None:
        self.client = Client()
        self.email1 = "login1@gmail.com"
        self.email2 = "login2@gmail.com"
        self.create_user(email=self.email1, password="abc123")
        self.create_user(email=self.email2, password="abc123")
        self.session1 = self.login(client=self.client, email=self.email1, password="abc123")
        self.session2 = self.login(client=self.client, email=self.email2, password="abc123")

    def call(self, method, session, data=None):
        if method == Method.get:
            return self.client.get(
                path=APIPath.transfer,
                **{"HTTP_SESSION": session}
            )
        elif method == Method.post:
            return self.client.post(
                path=APIPath.transfer,
                data=data,
                content_type='application/json',
                **{"HTTP_SESSION": session}
            )
        elif method == Method.put:
            return self.client.put(
                path=APIPath.transfer,
                data=data,
                content_type='application/json',
                **{"HTTP_SESSION": session}
            )

    def test_create_transfer(self):
        user = User.objects.get(email=self.email1)
        player = Player.objects.filter(team=user.team)[0]
        data = {
            "player_identifier": player.identifier,
            "price": 1500000
        }
        response = self.call(Method.post, self.session1, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        fields = ["player_identifier", "price"]
        for field in fields:
            self.assertTrue(field in data)
        self.assertEqual(len(data), len(fields))
        transfer = Transfer.objects.get(player__identifier=player.identifier)
        self.assertEqual(transfer.source_team, user.team)
        self.assertEqual(transfer.destination_team, None)
        self.assertEqual(transfer.price, 1500000)
        self.assertEqual(transfer.increase_percentage, None)

        response = self.call(Method.post, self.session1, data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_create_transfer_gets_403_if_player_not_in_team(self):
        user = User.objects.get(email=self.email1)
        player = Player.objects.filter(team=user.team)[0]
        data = {
            "player_identifier": player.identifier,
            "price": 1500000
        }
        response = self.call(Method.post, self.session2, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_transfer(self):
        user1 = User.objects.get(email=self.email1)
        user2 = User.objects.get(email=self.email2)
        player1_identifier = Player.objects.filter(team=user1.team)[0].identifier
        player2_identifier = Player.objects.filter(team=user2.team)[0].identifier
        data = {"player_identifier": player1_identifier, "price": 1500000}
        self.call(Method.post, self.session1, data)
        data["player_identifier"] = player2_identifier
        self.call(Method.post, self.session2, data)

        response1 = json.loads(self.call(Method.get, self.session1).content)
        response2 = json.loads(self.call(Method.get, self.session2).content)
        self.assertEqual(response1, response2)
        self.assertEqual(len(response1), 2)

    def test_update_transfer(self):
        user = User.objects.get(email=self.email1)
        player = Player.objects.filter(team=user.team)[0]
        data = {
            "player_identifier": player.identifier,
            "price": 1500000
        }
        self.call(Method.post, self.session1, data)
        data["price"] = 1200000
        response = self.call(Method.put, self.session1, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transfer = Transfer.objects.get(player__identifier=player.identifier)
        self.assertEqual(transfer.price, 1200000)

    def test_update_transfer_gets_403_if_player_not_in_team(self):
        user1 = User.objects.get(email=self.email1)
        user2 = User.objects.get(email=self.email2)
        player1_identifier = Player.objects.filter(team=user1.team)[0].identifier
        player2_identifier = Player.objects.filter(team=user2.team)[0].identifier
        data = {"player_identifier": player1_identifier, "price": 1500000}
        self.call(Method.post, self.session1, data)
        data["player_identifier"] = player2_identifier
        self.call(Method.post, self.session2, data)

        data["price"] = 1200000
        response = self.call(Method.put, self.session1, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)





