from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Chatty(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ⚡ Custom User
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin_message = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"


class Message(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    username = models.CharField(max_length=100)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}: {self.text[:20]}"

    @property
    def display_username(self):
        if self.user and self.user.is_superuser:
            return "Admin"
        return self.username

    @property
    def is_superuser(self):
        return self.user.is_superuser if self.user else False
