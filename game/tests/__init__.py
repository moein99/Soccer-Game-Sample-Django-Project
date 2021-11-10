import json

from game.api.helpers import generate_random_team, hash_func
from game.models import User


class APIPath:
    login = "/api/login"
    register = "/api/register"
    team = "/api/team"
    players = "/api/players"
    transfer = "/api/transfer"
    buy = "/api/buy"


class Method:
    get = "get"
    post = "post"
    put = "put"


class TestMixin:
    @staticmethod
    def create_user(email, password="abc123", team_name="", country=""):
        team = generate_random_team(team_name=team_name, country=country)
        return User.objects.create(email=email, password=hash_func(password), team=team)

    @staticmethod
    def login(client, email, password):
        data = {
            "email": email,
            "password": password,
        }
        response = client.post(
            path=APIPath.login,
            data=json.dumps(data),
            content_type='application/json'
        )
        return json.loads(response.content)["session_id"]
