from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from Sale.models import SaleItem, Sale
from payment.models import Card
from products.models import Product


class SaleItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class SaleCreateSerializer(serializers.Serializer):
    items = SaleItemInputSerializer(many=True)

    def validate(self, data):
        user = self.context['request'].user

        if not user.is_authenticated or not user.is_customer:
            raise serializers.ValidationError({"detail": "Siz customer emassiz, iltimos ro‘yxatdan o‘ting."})

        try:
            card = Card.objects.get(card_user=user)
        except Card.DoesNotExist:
            raise serializers.ValidationError({"detail": "Sizda karta mavjud emas."})

        data['customer'] = user
        data['card'] = card
        return data

    def create(self, validated_data):
        user = validated_data['customer']
        card = validated_data['card']
        items_data = validated_data['items']

        with transaction.atomic():
            sale = Sale.objects.create(customer=user, card_number=card.card_number)
            total = Decimal('0.00')

            for item in items_data:
                product = Product.objects.select_for_update().get(id=item['product_id'])

                if product.quantity < item['quantity']:
                    raise serializers.ValidationError({
                        "detail": f"{product.name} mahsuloti uchun yetarli miqdor yo‘q."
                    })

                SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price
                )

                product.quantity -= item['quantity']
                product.save(update_fields=['quantity'])

                total += product.price * item['quantity']

            if card.card_balance < total:
                raise serializers.ValidationError({
                    "detail": "Karta balansida yetarli mablag‘ yo‘q."
                })

            card.card_balance -= total
            card.save(update_fields=['card_balance'])

            sale.total_amount = total
            sale.save(update_fields=['total_amount'])

        return sale


from rest_framework import serializers
from .models import Sale, SaleItem


class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = SaleItem
        fields = ['product_name', 'product_price', 'quantity', 'price']


class SaleDetailSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    items = SaleItemSerializer(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = [
            'id',
            'customer_name',
            'card_number',
            'total_amount',
            'date',
            'items'
        ]
