import hashlib

import redis
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from game.models import Team, Player, PlayerRole, User

REDIS_POOL = redis.ConnectionPool(host=settings.REDIS["host"], port=settings.REDIS["port"], db=settings.REDIS["db"])


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        connection = get_redis_connection()
        session_id = request.headers.get("session")
        return session_id is not None and connection.get(session_id) is not None


class IsOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        user = get_user_from_request(request)
        return obj.team.id == user.team.id


def get_redis_connection():
    return redis.Redis(connection_pool=REDIS_POOL)


def get_user_from_request(request):
    email = get_redis_connection().get(request.headers["session"]).decode("utf-8")
    return get_object_or_404(User, email=email)


def generate_random_team(team_name="", country=""):
    team = Team.objects.create(name=team_name, country=country, balance=settings.TEAM["initial_balance"])
    players = []
    initial_setup = [
        (PlayerRole.GOAL_KEEPER, settings.TEAM["initial_goal_keepers"]),
        (PlayerRole.DEFENDER, settings.TEAM["initial_defenders"]),
        (PlayerRole.MID_FIELDER, settings.TEAM["initial_mid_fielders"]),
        (PlayerRole.ATTACKER, settings.TEAM["initial_attackers"]),
    ]
    for role, count in initial_setup:
        for _ in range(count):
            player = Player.generate_random()
            player.team = team
            player.role = role
            players.append(player)
    Player.objects.bulk_create(players)
    return team


def hash_func(string):
    return hashlib.md5(string.encode()).hexdigest()


