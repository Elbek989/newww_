from django.urls import path
from .views import SaleCreateView, SaleListView, SaleDetailView, CustomerSalesHistoryView

urlpatterns = [
    path('sales/', SaleListView.as_view(), name='sale-list'),
    path('sales/create/', SaleCreateView.as_view(), name='sale-create'),
    path('sales/<int:pk>/', SaleDetailView.as_view(), name='sale-detail'),
path('sales/history/', CustomerSalesHistoryView.as_view(), name='customer-sales-history'),
]
