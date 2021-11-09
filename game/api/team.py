from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets

from game.api.helpers import get_redis_connection, IsAuthenticated
from game.models import Team, User


class TeamGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'country', 'balance', 'value']


class TeamUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'country']


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamGetSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        email = get_redis_connection().get(self.request.headers["session"]).decode("utf-8")
        return get_object_or_404(User, email=email).team

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TeamGetSerializer
        elif self.action == 'update':
            return TeamUpdateSerializer
