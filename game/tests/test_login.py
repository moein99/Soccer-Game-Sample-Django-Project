import json

from django.conf import settings
from django.test import TestCase, Client
from rest_framework import status

from game.api.helpers import get_redis_connection


class RegisterTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.email = "login@gmail.com"
        register_data = {
            "email": self.email,
            "password": "abc123",
            "repeated_password": "abc123",
            "team_name": "Real Madrid",
            "team_country": "Spain",
        }
        self.client.post(
            path="/api/register",
            data=json.dumps(register_data),
            content_type='application/json'
        )

    def test_login(self):
        data = {
            "email": self.email,
            "password": "abc123",
        }
        response = self.client.post(
            path="/api/login",
            data=json.dumps(data),
            content_type='application/json'
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("timeout"), settings.REDIS["expire_amount"])
        connection = get_redis_connection()
        value_stored_in_redis = connection.get(data.get("session_id")).decode("utf-8")
        self.assertEqual(value_stored_in_redis, self.email)
