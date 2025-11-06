from rest_framework import generics, permissions
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartListView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

class CartAddItemView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)

class CartItemRemoveView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'item_id'

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart.items.all()
