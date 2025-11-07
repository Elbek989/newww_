from itertools import product

from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product
from rest_framework import serializers
from .models import CartItem

class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()


    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price','product_name',]

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity
    def get_product_name(self, obj):
        return obj.product.name



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']
