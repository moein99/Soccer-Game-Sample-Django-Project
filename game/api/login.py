import uuid

from django.conf import settings
from django.http import JsonResponse
from rest_framework import serializers, generics, status

from game.api.helpers import hash_func, get_redis_connection
from game.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(email=serializer.validated_data.get("email")).first()
        if (
                user is None or
                hash_func(serializer.validated_data.get("password")) != user.password
        ):
            return JsonResponse(data={"error": "email or password is wrong"}, status=status.HTTP_401_UNAUTHORIZED)
        redis_client = get_redis_connection()
        session_id = str(uuid.uuid4())
        redis_client.set(session_id, user.email, ex=settings.REDIS["expire_amount"])

        return JsonResponse(
            data={"session_id": session_id, "timeout": 3600},
            status=status.HTTP_200_OK
        )
