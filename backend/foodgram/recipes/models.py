from django.contrib.auth import get_user_model
from django.db import models

from .validators import validate_time

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=50,
        unique=True,
    )
    color = models.CharField(
        'Цвет',
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        'Слаг',
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingridient(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
        unique=True,
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=20,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    name = models.CharField(
        'Название',
        max_length=200
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
    )
    ingridients = models.ManyToManyField(
        Ingridient,
        verbose_name='Ингредиенты',
        through='IngridientAmount',
        related_name='recipes',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/'
    )
    text = models.TextField(
        'Описание',
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления',
        validators=(validate_time,)
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']


class IngridientAmount(models.Model):
    ingridient = models.ForeignKey(
        Ingridient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='ingridient_amount'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='ingridient_amount'
    )
    amount = models.DecimalField(
        'Количество',
        max_digits=6,
        decimal_places=2,
    )

    class Meta:
        verbose_name = 'Количество ингредиентов'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['ingridient', 'recipe'],
                name='unique_ingridient'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping'
            )
        ]
