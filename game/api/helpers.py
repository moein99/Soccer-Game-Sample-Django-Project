import hashlib

import redis
from django.conf import settings
from rest_framework.permissions import BasePermission

from game.models import Team, Player, Ownership, PlayerRole, User

REDIS_POOL = redis.ConnectionPool(host=settings.REDIS["host"], port=settings.REDIS["port"], db=settings.REDIS["db"])


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        connection = get_redis_connection()
        session_id = request.headers["session"]
        return connection.get(session_id) is not None


class IsOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        connection = get_redis_connection()
        session_id = request.headers["session"]
        email = connection.get(session_id).decode("utf-8")
        user = User.objects.get(email=email)
        return Ownership.objects.get(player=obj).team.id == user.team.id


def get_redis_connection():
    return redis.Redis(connection_pool=REDIS_POOL)


def generate_random_team(team_name="", country=""):
    team = Team.objects.create(name=team_name, country=country, balance=settings.TEAM["initial_balance"])
    for _ in range(settings.TEAM["initial_goal_keepers"]):
        player = Player.generate_random()
        Ownership.objects.create(team=team, player=player, role=PlayerRole.GOAL_KEEPER)
    for _ in range(settings.TEAM["initial_defenders"]):
        player = Player.generate_random()
        Ownership.objects.create(team=team, player=player, role=PlayerRole.DEFENDER)
    for _ in range(settings.TEAM["initial_mid_fielders"]):
        player = Player.generate_random()
        Ownership.objects.create(team=team, player=player, role=PlayerRole.MID_FIELDER)
    for _ in range(settings.TEAM["initial_attackers"]):
        player = Player.generate_random()
        Ownership.objects.create(team=team, player=player, role=PlayerRole.ATTACKER)
    return team


def hash_func(string):
    return hashlib.md5(string.encode()).hexdigest()


