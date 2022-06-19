# Generated by Django 2.2.19 on 2022-06-19 21:26

from django.db import migrations, models
import recipes.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20220618_0708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientamount',
            name='amount',
            field=models.PositiveIntegerField(validators=[recipes.validators.validate_time], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(validators=[recipes.validators.validate_ingredient_amount], verbose_name='Время приготовления'),
        ),
    ]
