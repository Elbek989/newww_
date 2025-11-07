from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response

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
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)

        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        if quantity > product.quantity:
            raise serializers.ValidationError({
                "detail": f"Not enough stock for {product.name}. "
                          f"Only {product.quantity} left."
            })

        existing_item = cart.items.filter(product=product).first()

        if existing_item:
            new_quantity = existing_item.quantity + quantity

            if new_quantity > product.quantity:
                raise serializers.ValidationError({
                    "detail": f"Not enough stock for {product.name}. "
                              f"You already have {existing_item.quantity} in cart, "
                              f"and only {product.quantity - existing_item.quantity} more available."
                })

            existing_item.quantity = new_quantity
            existing_item.save(update_fields=['quantity'])
            self.instance = existing_item
        else:
            self.instance = serializer.save(cart=cart)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            CartItemSerializer(self.instance).data,
            status=status.HTTP_201_CREATED
        )


class CartItemRemoveView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'item_id'

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart.items.all()
class CartUpdateItemView(generics.UpdateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'item_id'

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart.items.all()

    def perform_update(self, serializer):
        cart_item = serializer.instance
        new_quantity = serializer.validated_data.get('quantity', cart_item.quantity)
        product = cart_item.product

        if new_quantity > product.quantity:
            raise serializers.ValidationError({
                "detail": f"Not enough stock for {product.name}. "
                          f"Only {product.quantity} left."
            })

        serializer.save()
