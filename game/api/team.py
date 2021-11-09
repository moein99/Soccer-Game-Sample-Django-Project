from rest_framework import serializers, viewsets
from rest_framework.response import Response

from game.api.helpers import get_redis_connection, IsAuthenticated
from game.models import Team, User


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'country', 'balance', 'value']


class InspectTeamAPI(viewsets.ReadOnlyModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        email = get_redis_connection().get(self.request.headers["session"]).decode("utf-8")
        team = TeamSerializer(User.objects.get(email=email).team)
        return Response(team.data)
