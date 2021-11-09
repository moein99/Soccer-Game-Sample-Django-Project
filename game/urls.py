from django.urls import path

from game.api.login import LoginAPI
from game.api.players import PlayerViewSet
from game.api.register import RegisterAPI
from game.api.team import TeamViewSet

urlpatterns = [
    path('api/register', RegisterAPI.as_view(), name="register"),
    path('api/login', LoginAPI.as_view(), name="login"),
    path('api/team', TeamViewSet.as_view({'get': 'retrieve', 'post': 'update'}), name="team"),
    path('api/players', PlayerViewSet.as_view({'get': 'list', 'post': 'update'}), name="players"),
]
