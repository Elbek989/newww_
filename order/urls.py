from django.urls import path

from Karzinka.views import CartUpdateItemView
from .views import OrderListCreateView, OrderHistoryView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('history/', OrderHistoryView.as_view(), name='order-history'),


]
