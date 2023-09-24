from django.contrib import admin

from recipes.models import (Ingredient, Tag, Recipe, IngredientInRecipe,
                            Favorite, ShoppingCart)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)


class IngredientInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 0
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'author',
                    'text',
                    'cooking_time',)
    fields = ('name', 'text', 'author', 'image', 'tags', 'cooking_time')
    search_fields = ('name', 'subscribing__username')
    list_filter = ('author', 'tags')
    empty_value_display = '-пусто-'
    inlines = [IngredientInline]


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredients', 'amount')
    list_filter = ('recipe', 'ingredients')
    search_fields = ('recipe', 'ingredients')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_filter = ('user',)
    search_fields = ('user',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_filter = ('user',)
    search_fields = ('user',)
