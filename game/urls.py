from django.urls import path

from game.api.buy import BuyAPI
from game.api.login import LoginAPI
from game.api.players import PlayerViewSet
from game.api.register import RegisterViewSet
from game.api.team import TeamViewSet
from game.api.transfer import TransferViewSet

urlpatterns = [
    path('api/register', RegisterViewSet.as_view({'post': 'create'}), name="register"),
    path('api/login', LoginAPI.as_view(), name="login"),
    path('api/team', TeamViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name="team"),
    path('api/players', PlayerViewSet.as_view({'get': 'list'}), name="players"),
    path('api/players/<str:player_identifier>', PlayerViewSet.as_view({'put': 'update'}), name="players"),
    path('api/transfer', TransferViewSet.as_view({'get': 'list', 'post': 'create'}), name="transfer"),
    path('api/transfer/<str:player_identifier>', TransferViewSet.as_view({'put': 'update'}), name="transfer-update"),
    path('api/buy', BuyAPI.as_view(), name="buy"),
]
