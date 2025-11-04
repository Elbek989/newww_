from django.db import models

from user.models import User


class Card(models.Model):
    card_number = models.CharField(max_length=14, unique=True)
    card_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    card_user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_password = models.CharField(max_length=4)

    def __str__(self):
        return str(self.card_user.username)
