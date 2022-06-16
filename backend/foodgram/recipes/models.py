from django.contrib.auth import get_user_model
from django.db import models

from .validators import validate_time

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    color = models.CharField(
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        unique=True,
    )


class Ingridient(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
    )
    measurement_unit = models.CharField(
        max_length=20,
    )


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
    )
    ingridients = models.ManyToManyField(
        Ingridient,
        through='IngridientAmount',
        related_name='recipes',
    )
    image = models.ImageField(
        upload_to='recipes/'
    )
    text = models.TextField()
    cooking_time = models.PositiveIntegerField(
        validators=(validate_time,)
    )

    class Meta:
        ordering = ['-pub_date']


class IngridientAmount(models.Model):
    ingridient = models.ForeignKey(
        Ingridient,
        on_delete=models.CASCADE,
        related_name='ingridient_amount'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingridient_amount'
    )
    amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingridient', 'recipe'],
                name='unique_ingridient'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping'
            )
        ]
