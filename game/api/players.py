from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets

from game.api.helpers import IsAuthenticated, get_redis_connection, IsOwner
from game.models import Player, User, Ownership


class PlayerGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['identifier', 'first_name', 'last_name', 'country', 'age', 'market_value']


class PlayerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['identifier', 'first_name', 'last_name', 'country']


class PlayerViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerGetSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_serializer_class(self):
        if self.action == "list":
            return PlayerGetSerializer
        elif self.action == "update":
            return PlayerUpdateSerializer

    def get_queryset(self):
        email = get_redis_connection().get(self.request.headers["session"]).decode("utf-8")
        user = User.objects.get(email=email)
        return [item.player for item in Ownership.objects.filter(team=user.team).select_related("player")]

    def get_object(self):
        player_identifier = self.request.data["identifier"]
        player = get_object_or_404(Player, identifier=player_identifier)
        self.check_object_permissions(self.request, player)
        return player
