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
        return self.player_set.all().aggregate(Sum("market_value")).get("market_value__sum")


class PlayerRole:
    GOAL_KEEPER = "gk"
    DEFENDER = "de"
    MID_FIELDER = "mf"
    ATTACKER = "at"


class Player(models.Model):
    identifier = models.CharField(default=get_random_string, max_length=12)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=30)
    age = models.IntegerField()
    market_value = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    ROLE_OPTIONS = (
        (PlayerRole.GOAL_KEEPER, "Goal Keeper"),
        (PlayerRole.DEFENDER, "Defender"),
        (PlayerRole.MID_FIELDER, "Mid Fielder"),
        (PlayerRole.ATTACKER, "Attacker"),
    )
    role = models.CharField(max_length=2, choices=ROLE_OPTIONS)

    @staticmethod
    def generate_random():
        return Player(
            first_name=random.choice(RANDOM_FIRST_NAMES),
            last_name=random.choice(RANDOM_LAST_NAMES),
            country=random.choice(RANDOM_COUNTRIES),
            age=random.randint(settings.PLAYER["start_age"], settings.PLAYER["end_age"]),
            market_value=settings.PLAYER["initial_market_value"]
        )


class User(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=40)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class Transfer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    source_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="source_set")
    destination_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="destination_set",
                                         default=None, null=True)
    price = models.IntegerField()
    increase_percentage = models.IntegerField(default=None, null=True)


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

