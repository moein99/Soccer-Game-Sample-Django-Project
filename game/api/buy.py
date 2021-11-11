import random

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers, status

from game.api import SessionRequiredMixin
from game.api.helpers import get_user_from_request
from game.models import Transfer


class BuyPlayerSerializer(serializers.Serializer):
    player_identifier = serializers.CharField(max_length=12)


class BuyAPI(generics.GenericAPIView, SessionRequiredMixin):
    serializer_class = BuyPlayerSerializer

    def get_object(self):
        return get_object_or_404(
            Transfer,
            destination_team__isnull=True,
            player__identifier=self.request.data["player_identifier"]
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transfer = self.get_object()
        user = get_user_from_request(request)
        if user.team.id == transfer.player.team.id:
            return JsonResponse(
                data={"error:": "you already own this player"},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif user.team.balance < transfer.price:
            return JsonResponse(
                data={"error:": "your team balance is less than the player's price"},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.do_transfer(user.team, transfer)
        return JsonResponse({}, status=status.HTTP_200_OK)

    @staticmethod
    def do_transfer(team, transfer):
        source_team = transfer.source_team
        destination_team = team
        transfer.destination_team = destination_team
        player = transfer.player
        player.team = team
        transfer.increase_percentage = random.randrange(10, 101)
        player.market_value = int(player.market_value + player.market_value * transfer.increase_percentage / 100)
        source_team.balance += transfer.price
        destination_team.balance -= transfer.price
        with transaction.atomic():
            player.save()
            source_team.save()
            destination_team.save()
            transfer.save()
