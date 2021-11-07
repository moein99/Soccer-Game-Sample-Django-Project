from django.db import models
from django.db.models import Sum
from django.utils.functional import cached_property


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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=30)
    age = models.IntegerField()
    market_value = models.IntegerField()


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
    password = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
