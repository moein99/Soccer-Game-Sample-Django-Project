import json

from django.test import TestCase, Client
from rest_framework import status

from game.models import User
from game.tests import TestMixin, Method, APIPath


class TeamTestCase(TestCase, TestMixin):
    def setUp(self) -> None:
        self.client = Client()
        self.email = "login@gmail.com"
        self.create_user(email=self.email, password="abc123")
        self.session = self.login(client=self.client, email=self.email, password="abc123")

    def call(self, method, session, data=None):
        if method == Method.get:
            return self.client.get(
                path=APIPath.team,
                **{"HTTP_SESSION": session}
            )
        elif method == Method.put:
            return self.client.put(
                path=APIPath.team,
                data=json.dumps(data),
                content_type='application/json',
                **{"HTTP_SESSION": session}
            )

    def test_get_team(self):
        response = self.call(Method.get, self.session)
        data = json.loads(response.content)
        fields = ['name', 'country', 'balance', 'value']
        for field in fields:
            self.assertTrue(field in data)
        self.assertEqual(len(data), len(fields))

    def test_update_team(self):
        data = {
            "name": "New Real Madrid",
            "country": "USA",
        }
        response = self.call(method=Method.put, session=self.session, data=data)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        update_fields = ['name', 'country']
        for field in update_fields:
            self.assertTrue(field in data)
        team = User.objects.get(email=self.email).team
        self.assertEqual(team.name, "New Real Madrid")
        self.assertEqual(team.country, "USA")

