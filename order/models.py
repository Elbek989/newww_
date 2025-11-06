from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=50)
    payment_type = models.CharField(max_length=50)
    card = models.CharField(max_length=50, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


from django.db import models


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    product = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product} (x{self.quantity}) - {self.total_price} so'm"
