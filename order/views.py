from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer
from Karzinka.models import Cart, CartItem
from payment.models import Card


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            raise serializers.ValidationError({"detail": "Cart is empty."})

        cart_items = cart.items.all()
        if not cart_items.exists():
            raise serializers.ValidationError({"detail": "Cart is empty."})

        total_price = sum(item.quantity * item.product.price for item in cart_items)

        try:
            card = Card.objects.get(card_user=user)
        except Card.DoesNotExist:
            raise serializers.ValidationError({"detail": "You have no payment card."})

        if card.card_balance < total_price:
            raise serializers.ValidationError({"detail": "Insufficient balance."})

        card.card_balance -= total_price
        card.save(update_fields=['card_balance'])

        order = serializer.save(
            user=user,
            total_price=total_price,
            delivery_price=0,
            discount_price=0,
            status='pending',
            payment_type=self.request.data.get('payment_type', 'cash')
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                total_price=item.quantity * item.product.price
            )

        cart.items.all().delete()
class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')