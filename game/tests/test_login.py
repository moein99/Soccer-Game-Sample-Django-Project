import json

from django.conf import settings
from django.test import TestCase, Client
from rest_framework import status

from game.api.helpers import get_redis_connection
from game.tests import TestMixin, APIPath


class LoginTestCase(TestCase, TestMixin):
    def setUp(self) -> None:
        self.client = Client()
        self.email = "login@gmail.com"
        self.password = "abc123"
        self.create_user(email=self.email, password=self.password)

    def call(self, data):
        return self.client.post(
            path=APIPath.login,
            data=json.dumps(data),
            content_type='application/json'
        )

    def test_login(self):
        data = {
            "email": self.email,
            "password": self.password,
        }
        response = self.call(data=data)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("timeout"), settings.REDIS["expire_amount"])
        connection = get_redis_connection()
        value_stored_in_redis = connection.get(data.get("session_id")).decode("utf-8")
        self.assertEqual(value_stored_in_redis, self.email)

    def test_login_wrong_credentials(self):
        data = {
            "email": self.email,
            "password": self.password + "a",
        }
        response = self.call(data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        data["email"] = "newEmail@gmail.com"
        response = self.call(data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

