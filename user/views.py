from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import *
from products.make_token import get_user_token_from_serializer
from user.serializers import LoginSerializer, UserSerializer


class LoginView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        data = get_user_token_from_serializer(serializer)
        return Response(data, status=status.HTTP_200_OK)


from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status, generics, serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CustomerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


from rest_framework.authtoken.models import Token


class CustomerLoginView(generics.GenericAPIView):
    serializer_class = CustomerLoginSerializer

    @swagger_auto_schema(
        request_body=CustomerLoginSerializer,
        responses={
            200: openapi.Response("Login successful"),
            401: openapi.Response("Invalid credentials"),
            403: openapi.Response("You are not a customer")
        }
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"detail": "Invalid credentials"}, status=401)

        if not user.is_customer:
            return Response({"detail": "You are not a customer"}, status=403)

        token, _ = Token.objects.get_or_create(user=user)

        user.is_active = True
        user.save(update_fields=['is_active'])

        return Response({
            "detail": "Login successful",
            "user": user.username,
            "token": token.key
        }, status=200)


class UserRegisterView(APIView):
    permission_classes = []

    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
