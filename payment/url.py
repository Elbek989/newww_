from django.urls import path
from .views import CardListCreateView, CardDeleteView

urlpatterns = [
    path('cards/', CardListCreateView.as_view(), name='card-list-create'),
    path('cards/<int:id>/delete/', CardDeleteView.as_view(), name='card-delete'),
]
