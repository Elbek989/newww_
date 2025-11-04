from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from rest_framework import status
from .models import Card
from payment.serializer import CardSerializer


class CardListCreateView(generics.ListCreateAPIView):
    serializer_class = CardSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated or not user.is_customer or not user.is_active:
            return Card.objects.none()
        return Card.objects.filter(card_user=user)

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated or not user.is_customer or not user.is_active:
            raise serializers.ValidationError({"detail": "Only active customers can create cards."})
        serializer.save(card_user=user)


class CardDeleteView(generics.DestroyAPIView):
    serializer_class = CardSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated or not user.is_customer or not user.is_active:
            return Card.objects.none()
        return Card.objects.filter(card_user=user)
