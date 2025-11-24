# user/views.py

import random
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from django.views.generic import TemplateView

from .models import Chatty
from .serializers import LoginSerializer, RegisterSerializer, VerifyOTPSerializer, Chat

User = get_user_model()


class LoginView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({"detail": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        user.is_active = True
        user.save(update_fields=['is_active'])

        return Response({
            "detail": "Login successful",
            "user": user.username,
            "token": token.key
        }, status=200)


class RegisterAPIView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        otp_code = str(random.randint(100000, 999999))
        print(f"OTP for {email}: {otp_code}")
        cache.set(f"{email}_otp", otp_code, 600)
        cache.set(f"{email}_password", make_password(password), 600)

        return Response({"detail": "OTP yuborildi."}, status=status.HTTP_200_OK)


class VerifyOTPAPIView(APIView):
    @swagger_auto_schema(request_body=VerifyOTPSerializer)
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        cached_otp = cache.get(f"{email}_otp")
        cached_password = cache.get(f"{email}_password")

        if not cached_otp:
            return Response({"detail": "OTP muddati tugagan."}, status=status.HTTP_400_BAD_REQUEST)
        if otp != cached_otp:
            return Response({"detail": "Noto'g'ri OTP."}, status=status.HTTP_400_BAD_REQUEST)

        user = User(username=email, email=email, password=cached_password, is_active=True)
        user.save()
        cache.delete(f"{email}_otp")
        cache.delete(f"{email}_password")

        return Response({"detail": "Foydalanuvchi yaratildi", "user": user.email}, status=status.HTTP_201_CREATED)


class CustomerChattyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=Chat)
    def post(self, request):
        serializer = Chat(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat = Chatty.objects.create(text=serializer.validated_data['text'], username=request.user)
        return Response({"detail": "Chat yaratildi", "id": chat.id}, status=status.HTTP_201_CREATED)

    def get(self, request):
        chats = Chatty.objects.filter(username=request.user)
        serializer = Chat(chats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=Chat)
    def put(self, request, chat_id):
        try:
            chat = Chatty.objects.get(id=chat_id, username=request.user)
        except Chatty.DoesNotExist:
            return Response({"detail": "Chat topilmadi yoki ruxsat yo‘q."}, status=status.HTTP_404_NOT_FOUND)

        serializer = Chat(chat, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Chat yangilandi"}, status=status.HTTP_200_OK)

    def delete(self, request, chat_id):
        try:
            chat = Chatty.objects.get(id=chat_id, username=request.user)
        except Chatty.DoesNotExist:
            return Response({"detail": "Chat topilmadi yoki ruxsat yo‘q."}, status=status.HTTP_404_NOT_FOUND)

        chat.delete()
        return Response({"detail": "Chat o‘chirildi"}, status=status.HTTP_204_NO_CONTENT)


class ChatLoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"detail": "Email va password kiritilishi kerak"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "detail": "Login muvaffaqiyatli"
            })
        else:
            return Response({"detail": "Email yoki password xato"}, status=status.HTTP_401_UNAUTHORIZED)


class LoginPageView(TemplateView):
    template_name = "login.html"


class LoginSubmitView(TemplateView):
    template_name = "login.html"

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/users/chat-page/")

        return render(request, "login.html", {
            "error": "Email yoki parol noto‘g‘ri!"
        })


class ChatPageView(TemplateView):
    template_name = "chat.html"

    def get_context_data(self, **kwargs):
        context = super(ChatPageView, self).get_context_data(**kwargs)

        return context


from django.http import JsonResponse
from .models import Message


def get_messages(request):
    messages = Message.objects.order_by("timestamp")[:200]

    return JsonResponse({
        "messages": [
            {
                "username": "Admin" if m.is_superuser else m.username,
                "is_superuser": m.is_superuser,
                "text": m.text
            }
            for m in messages
        ]
    })
