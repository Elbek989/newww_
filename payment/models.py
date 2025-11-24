from django.db import models
from django.conf import settings  # << bu muhim

class Card(models.Model):
    card_number = models.CharField(max_length=14, unique=True)
    card_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    card_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # << bu auth.User o‘rniga ishlatiladi
        on_delete=models.CASCADE
    )
    expire_date = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.card_user.username} - {self.card_number}"
