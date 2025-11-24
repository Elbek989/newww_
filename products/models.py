from django.db import models

class Supermarket(models.Model):
    name = models.CharField(max_length=100)
    call_number = models.CharField(max_length=13)
    email = models.EmailField(max_length=100)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name0

class ProductTypes(models.TextChoices):
    SIMPLE = 'simple', "SIMPLE"
    LUXURY = 'lux', "LUX"

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    supermarket = models.ForeignKey(Supermarket, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    product_id = models.IntegerField(unique=True)
    product_type = models.CharField(choices=ProductTypes.choices, max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name
