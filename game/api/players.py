from rest_framework import serializers, viewsets

from game.api.helpers import IsAuthenticated, get_redis_connection
from game.models import Player, User, Ownership


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['identifier', 'first_name', 'last_name', 'country', 'age', 'market_value']


class InspectPlayersAPI(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlayerSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        email = get_redis_connection().get(self.request.headers["session"]).decode("utf-8")
        user = User.objects.get(email=email)
        return [item.player for item in Ownership.objects.filter(team=user.team).select_related("player")]
