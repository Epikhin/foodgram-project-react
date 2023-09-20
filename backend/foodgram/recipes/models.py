from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


User = get_user_model()


class Ingredient(models.Model):
    """Модель ингредиентов для рецептов"""

    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200,
    )

    class Meta:
        verbose_name = 'Ингредиент',
        verbose_name_plural = 'Ингредиенты',

    def __str__(self):
        return self.name


def validate_color_length(value):
    if not (len(value) == 7 and value.startswith('#')):
        raise ValidationError(
            'Цвет должен быть в формате "#RRGGBB" и иметь длину 7 символов.')


class Tag(models.Model):
    """Модель тэгов для рецептов"""

    name = models.CharField(
        verbose_name='Название тэга',
        max_length=200,
    )
    color = models.CharField(
        verbose_name='Цвет тэга',
        max_length=7,
        validators=[validate_color_length],
    )
    slug = models.SlugField(
        verbose_name='Слаг тэга',
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тэг',
        verbose_name_plural = 'Тэги',

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта"""

    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        default=None,
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='media/',
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='Ингредиенты',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[
            MinValueValidator(
                1, message='Минимальное значение - 1 минута'
            ),
            MaxValueValidator(
                812, message='Максимальное значение - 812 минут'
            ),
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации рецепта',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Рецепт',
        verbose_name_plural = 'Рецепты',
        ordering = ('-pub_date'),

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    """Модель для связи ингредиентов и рецептов"""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredients_in_recipe',
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ingredients_in_recipe',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                1, message='Минимальное количество - 1'
            ),
        ],
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте',
        verbose_name_plural = 'Ингредиенты в рецепте',

    def __str__(self):
        return (f'{self.ingredients.name} в количестве {self.amount}'
                f'{self.ingredients.measurement_unit}'
                f' в рецепте {self.recipe.name}')


class Favorite(models.Model):
    """Модель для избранных рецептов"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorites',
    )

    class Meta:
        verbose_name = 'Избранное',
        verbose_name_plural = 'Избранные',
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном {self.user}'


class ShoppingCart(models.Model):
    """Модель для списка покупок"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shopping_cart',
    )

    class Meta:
        verbose_name = 'Корзина',
        verbose_name_plural = 'Корзины',
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в корзине {self.user}'
