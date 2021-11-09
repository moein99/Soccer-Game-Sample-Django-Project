import random

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.utils.functional import cached_property
from django.utils.crypto import get_random_string


class Team(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=30)
    balance = models.IntegerField()

    @cached_property
    def value(self):
        return Ownership.objects.filter(
            team=self
        ).aggregate(Sum("player__market_value")).get("player__market_value__sum")


class Player(models.Model):
    identifier = models.CharField(default=get_random_string, max_length=12)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=30)
    age = models.IntegerField()
    market_value = models.IntegerField()

    @staticmethod
    def generate_random():
        return Player.objects.create(
            first_name=random.choice(RANDOM_FIRST_NAMES),
            last_name=random.choice(RANDOM_LAST_NAMES),
            country=random.choice(RANDOM_COUNTRIES),
            age=random.randint(settings.PLAYER["start_age"], settings.PLAYER["end_age"]),
            market_value=settings.PLAYER["initial_market_value"]
        )


class PlayerRole:
    GOAL_KEEPER = "gk"
    DEFENDER = "de"
    MID_FIELDER = "mf"
    ATTACKER = "at"


class Ownership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.OneToOneField(Player, on_delete=models.CASCADE)

    ROLE_OPTIONS = (
        (PlayerRole.GOAL_KEEPER, "Goal Keeper"),
        (PlayerRole.DEFENDER, "Defender"),
        (PlayerRole.MID_FIELDER, "Mid Fielder"),
        (PlayerRole.ATTACKER, "Attacker"),
    )
    role = models.CharField(max_length=2, choices=ROLE_OPTIONS)


class User(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=40)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


RANDOM_FIRST_NAMES = [
    "Leonel",
    "Jarrett",
    "Rogelio",
    "London",
    "Yareli",
    "Antonio",
    "Keyon",
    "Arabella",
    "Fletcher",
    "Roland",
    "Leland",
    "Isiah",
    "Alma",
    "Arely",
    "Noemi",
    "Jacob",
    "Summer",
    "Gabrielle",
    "Yosef",
    "Elianna",
]

RANDOM_LAST_NAMES = [
    "Cross",
    "Payne",
    "Hall",
    "Norton",
    "Patel",
    "Arroyo",
    "Tate",
    "Rowland",
    "Donovan",
    "Alvarez",
    "Kemp",
    "Barajas",
    "Schwartz",
    "Ruiz",
    "Bernard",
    "Cooley",
    "Henderson",
    "Joseph",
    "Santiago",
    "Cruz",
]

RANDOM_COUNTRIES = ["USA", "Canada", "Albania", "Belgium", "Japan", "Russia"]

