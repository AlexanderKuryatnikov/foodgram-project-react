from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator()],
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)


User = get_user_model()


class Subscribtion(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber'
    )
    subscribed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subscribed'],
                name='unique_subsrcibtion'
            )
        ]
