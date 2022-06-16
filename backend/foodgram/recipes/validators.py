from django.core.exceptions import ValidationError


def validate_time(time):
    if time <= 0:
        raise ValidationError(
            'Время приготовления не может отрицательным или нулевым')
