from django.db import models
from products.models import Product


class Sale(models.Model):
    customer = models.ForeignKey(
        to='user.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    card_number = models.CharField(max_length=14)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Sale #{self.id} - {self.card_number}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
