from django.urls import path
from .views import *

urlpatterns = [

    path("Login/", LoginView.as_view(), name="LoginToken"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("verify-otp/", VerifyOTPAPIView.as_view(), name="verify-otp"),
    path("chat-login/", ChatLoginAPIView.as_view(), name="chat-login"),
    path("chat-api/", CustomerChattyAPIView.as_view(), name="chatty-api"),

    path("login-submit/", LoginSubmitView.as_view(), name="login-submit"),
    path("api/messages/", get_messages),

    path("chat-page/", ChatPageView.as_view(), name="chat-page"),
]
