import json

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open(
                'recipes/data/ingredients.json', 'r',
                encoding='UTF-8'
        ) as ingredients:
            ingredient_data = json.loads(ingredients.read())
            for ingredients in ingredient_data:
                Ingredient.objects.get_or_create(**ingredients)
        self.stdout.write(self.style.SUCCESS('Данные загружены'))
