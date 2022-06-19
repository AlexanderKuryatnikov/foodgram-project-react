import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(f'{settings.BASE_DIR}/data/ingredients.csv',
                  'r', encoding='utf-8') as ingredients_file:
            reader = csv.reader(ingredients_file)
            Ingredient.objects.bulk_create([
                Ingredient(name=name, measurement_unit=measurement_unit)
                for name, measurement_unit in reader
            ])
