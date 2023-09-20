from django_filters.rest_framework import FilterSet, filters
import django_filters
from recipes.models import Ingredient, Tag, Recipe
from users.models import User


class StartsWithCharFilter(django_filters.CharFilter):
    def filter(self, queryset, value):
        if value:
            return queryset.filter(
                **{f"{self.field_name}__istartswith": value})
        return queryset


class IngredientFilter(django_filters.FilterSet):
    name = StartsWithCharFilter()

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeFilter(FilterSet):
    author = filters.ModelChoiceFilter(
        field_name='author',
        queryset=User.objects.all()
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        if value:
            if self.request.user.is_authenticated:
                return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            if self.request.user.is_authenticated:
                return queryset.filter(shopping_cart__user=self.request.user)
        return queryset
