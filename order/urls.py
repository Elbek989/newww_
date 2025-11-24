from django.urls import path
from django.views.generic import TemplateView

from Karzinka.views import CartUpdateItemView
from user.views import ChatLoginAPIView
from .views import OrderListCreateView, OrderHistoryView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('history/', OrderHistoryView.as_view(), name='order-history'),


]
