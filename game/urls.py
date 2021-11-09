from django.urls import path

from game.api.buy import BuyAPI
from game.api.login import LoginAPI
from game.api.players import PlayerViewSet
from game.api.register import RegisterAPI
from game.api.team import TeamViewSet
from game.api.transfer import TransferViewSet

urlpatterns = [
    path('api/register', RegisterAPI.as_view(), name="register"),
    path('api/login', LoginAPI.as_view(), name="login"),
    path('api/team', TeamViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name="team"),
    path('api/players', PlayerViewSet.as_view({'get': 'list', 'put': 'update'}), name="players"),
    path('api/transfer', TransferViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'}), name="transfer"),
    path('api/transfer/buy', BuyAPI.as_view(), name="buy"),
]
