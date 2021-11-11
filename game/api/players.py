from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets

from game.api import SessionRequiredMixin
from game.api.helpers import get_redis_connection, IsPlayerOwner
from game.models import Player, User


class PlayerGetSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="get_display_role")

    class Meta:
        model = Player
        fields = ['identifier', 'first_name', 'last_name', 'role', 'country', 'age', 'market_value']


class PlayerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'country']


class PlayerViewSet(viewsets.ModelViewSet, SessionRequiredMixin):
    serializer_class = PlayerGetSerializer
    permission_classes = (IsPlayerOwner,)

    def get_serializer_class(self):
        if self.action == "list":
            return PlayerGetSerializer
        elif self.action == "update":
            return PlayerUpdateSerializer

    def get_queryset(self):
        email = get_redis_connection().get(self.request.headers["session"]).decode("utf-8")
        user = User.objects.get(email=email)
        return Player.objects.filter(team=user.team)

    def get_object(self):
        player_identifier = self.kwargs["player_identifier"]
        player = get_object_or_404(Player, identifier=player_identifier)
        self.check_object_permissions(self.request, player)
        return player
