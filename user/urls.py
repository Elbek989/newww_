from django.urls import path
from user.views import LoginView, CustomerLoginView, UserRegisterView

urlpatterns = [
    path('Login/', LoginView.as_view(), name='LoginToken'),
    path('customer/login/', CustomerLoginView.as_view(), name='customer-login'),
    path('customer/register/', UserRegisterView.as_view(), name='user-register'), ]
