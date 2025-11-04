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
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE)
    description = models.TextField()
    product_id = models.IntegerField()

    def __str__(self):
        return self.name


class Users(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class Customer(models.Model):
    name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=14)
    card_password = models.CharField(max_length=4)

    def __str__(self):
        return self.name

# Create your models here.
