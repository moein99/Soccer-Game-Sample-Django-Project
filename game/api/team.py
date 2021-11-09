from rest_framework import serializers, viewsets

from game.api.helpers import IsAuthenticated, get_user_from_request
from game.models import Team


class TeamGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'country', 'balance', 'value']


class TeamUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'country']


class TeamViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = get_user_from_request(self.request)
        return user.team

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TeamGetSerializer
        elif self.action == 'update':
            return TeamUpdateSerializer
