from django.db import transaction
from rest_framework import serializers, viewsets

from game.api.helpers import generate_random_team, hash_func
from game.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100)
    repeated_password = serializers.CharField(max_length=100)
    team_name = serializers.CharField(max_length=100)
    team_country = serializers.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('email', 'password', 'repeated_password', 'team_name', 'team_country')

    def validate_repeated_password(self, repeated_password):
        if repeated_password != self.initial_data.get("password"):
            raise serializers.ValidationError("password and repeated_password do not match")

    def create(self, validated_data):
        with transaction.atomic():
            team = generate_random_team(team_name=validated_data["team_name"], country=validated_data["team_country"])
            user = User.objects.create(
                email=validated_data['email'],
                password=hash_func(validated_data['password']),
                team=team
            )
        return user

    def to_representation(self, obj):
        return {"email": obj.email}


class RegisterViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
