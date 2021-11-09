import json

from django.test import TestCase, Client


class TeamTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.register()
        self.session = self.login()

    def register(self):
        register_data = {
            "email": "login@gmail.com",
            "password": "abc123",
            "repeated_password": "abc123",
            "team_name": "real madrid",
            "team_country": "spain",
        }
        self.client.post(
            path="/api/register",
            data=json.dumps(register_data),
            content_type='application/json'
        )

    def login(self):
        data = {
            "email": "login@gmail.com",
            "password": "abc123",
        }
        response = self.client.post(
            path="/api/login",
            data=json.dumps(data),
            content_type='application/json'
        )
        return json.loads(response.content)["session_id"]

    def test_team(self):
        response = self.client.get(
            path="/api/team",
            **{"HTTP_SESSION": self.session}
        )
        data = json.loads(response.content)
        fields = ['name', 'country', 'balance', 'value']

        for field in fields:
            self.assertTrue(field in data)
        self.assertEqual(len(data), len(fields))
