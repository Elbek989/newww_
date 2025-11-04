from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token


def get_user_token_from_serializer(serializer):
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get("username")
    password = serializer.validated_data.get("password")

    user = authenticate(username=username, password=password)
    if user is None or not user.is_active:
        raise AuthenticationFailed("Username or password is incorrect")

    token, created = Token.objects.get_or_create(user=user)
    return {"token": token.key, "username": user.username}
