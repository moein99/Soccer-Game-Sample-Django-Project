from django.core.validators import MinValueValidator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets, status

from game.api.helpers import IsAuthenticated, get_user_from_request, IsOwner
from game.models import Transfer, Player


class GetTransferSerializer(serializers.ModelSerializer):
    identifier = serializers.CharField(max_length=12, source="player.identifier")
    first_name = serializers.CharField(source="player.first_name")
    last_name = serializers.CharField(source="player.last_name")
    team_name = serializers.CharField(source="source_team.name")
    country = serializers.CharField(source="player.country")
    age = serializers.CharField(source="player.age")
    market_value = serializers.IntegerField(source="player.market_value")
    price = serializers.IntegerField()

    class Meta:
        model = Transfer
        fields = ['identifier', 'first_name', 'last_name', 'team_name', 'country',
                  'age', 'market_value', 'price']


class CreateTransferSerializer(serializers.ModelSerializer):
    player_identifier = serializers.CharField(max_length=12, source="player.identifier")
    price = serializers.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        model = Transfer
        fields = ["player_identifier", "price"]

    def create(self, validated_data):
        user = get_user_from_request(self.context["request"])
        player = get_object_or_404(Player, identifier=validated_data["player"]["identifier"])
        transfer = Transfer.objects.filter(player=player, source_team=user.team, destination_team=None)
        if not transfer.exists():
            return Transfer.objects.create(player=player, source_team=user.team, price=validated_data["price"])
        raise AlreadyExistException()


class UpdateTransferSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        model = Transfer
        fields = ["price"]

    def update(self, instance, validated_data):
        instance.price = validated_data["price"]
        instance.save()
        return instance


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.filter(destination_team__isnull=True)
    permission_classes = (IsAuthenticated, IsOwner)

    def get_object(self):
        player = self.__check_user_permission(player_identifier=self.kwargs["player_identifier"])
        return get_object_or_404(Transfer, player=player, destination_team__isnull=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return GetTransferSerializer
        elif self.action == 'create':
            return CreateTransferSerializer
        elif self.action == "update":
            return UpdateTransferSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.__check_user_permission(serializer.validated_data["player"]["identifier"])
        try:
            serializer.save()
        except AlreadyExistException:
            return JsonResponse({"error": "transfer already exists."}, status=status.HTTP_409_CONFLICT)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    def __check_user_permission(self, player_identifier):
        player = get_object_or_404(Player, identifier=player_identifier)
        self.check_object_permissions(self.request, player)
        return player


class AlreadyExistException(Exception):
    pass
