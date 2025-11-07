from rest_framework import serializers
from .models import Order, OrderItem
from Karzinka.models import CartItem
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'total_price']



class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'payment_type', 'total_price']
        read_only_fields = ['user', 'total_price', 'delivery_price', 'discount_price','status']
