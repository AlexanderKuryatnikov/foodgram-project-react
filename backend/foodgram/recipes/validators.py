from django.core.exceptions import ValidationError


def validate_time(time):
    if time <= 0:
        raise ValidationError(
            'Время приготовления не может отрицательным или нулевым')


def validate_ingredient_amount(amount):
    if amount <= 0:
        raise ValidationError(
            'Количество ингредиента не может отрицательным или нулевым')
