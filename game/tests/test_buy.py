from django.conf import settings
from django.test import TestCase, Client
from rest_framework import status

from game.models import User, Player, Transfer
from game.tests import TestMixin, APIPath


class TransferTestCase(TestCase, TestMixin):
    def setUp(self) -> None:
        self.client = Client()
        self.email1 = "login1@gmail.com"
        self.email2 = "login2@gmail.com"
        self.create_user(email=self.email1, password="abc123")
        self.create_user(email=self.email2, password="abc123")
        self.session1 = self.login(client=self.client, email=self.email1, password="abc123")
        self.session2 = self.login(client=self.client, email=self.email2, password="abc123")
        self.create_transfers()

    def call(self, data, session):
        return self.client.post(
            path=APIPath.buy,
            data=data,
            content_type='application/json',
            **{"HTTP_SESSION": session}
        )

    def create_transfers(self):
        user1 = User.objects.get(email=self.email1)
        user2 = User.objects.get(email=self.email2)
        for player in Player.objects.filter(team=user1.team)[:5]:
            Transfer.objects.create(player=player, source_team=user1.team, price=1200000)
        for player in Player.objects.filter(team=user2.team)[:5]:
            Transfer.objects.create(player=player, source_team=user2.team, price=1200000)

    def test_buy(self):
        team1 = User.objects.get(email=self.email1).team
        team2 = User.objects.get(email=self.email2).team
        transfer = Transfer.objects.filter(source_team=team2)[0]
        player_in_second_team = transfer.player
        data = {"player_identifier": player_in_second_team.identifier}
        response = self.call(data, self.session1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        team1.refresh_from_db()
        team2.refresh_from_db()
        player_in_second_team.refresh_from_db()
        transfer.refresh_from_db()
        self.assertEqual(team1.balance, 3800000)
        self.assertEqual(team2.balance, 6200000)
        self.assertTrue(transfer.destination_team is not None)
        self.assertTrue(transfer.increase_percentage is not None)
        self.assertEqual(
            player_in_second_team.market_value,
            int(settings.PLAYER["initial_market_value"] + settings.PLAYER["initial_market_value"] * transfer.increase_percentage / 100)
        )
        self.assertEqual(player_in_second_team.team, team1)

    def test_buy_bad_requests(self):
        player_id_in_first_team = Transfer.objects.filter(
            source_team=User.objects.get(email=self.email1).team
        )[0].player.identifier
        data = {"player_identifier": player_id_in_first_team}
        response = self.call(data, self.session1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        team = User.objects.get(email=self.email1).team
        team.balance = 0
        team.save()
        player_id_in_second_team = Transfer.objects.filter(
            source_team=User.objects.get(email=self.email2).team
        )[0].player.identifier
        data = {"player_identifier": player_id_in_second_team}
        response = self.call(data, self.session1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


