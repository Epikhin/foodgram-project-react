from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum, F
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Recipe, Ingredient, Tag, Favorite, ShoppingCart
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          TagSerializer,
                          RecipeOnlyReadSerializer, ShoppingCartSerializer,
                          RecipeWriteSerializer)
from .permissions import (IsAdminOrReadOnly, IsAuthorOrReadOnly,
                          IsAuthenticatedOrReadOnly)

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related(
        'author').prefetch_related('ingredients_in_recipe').all()
    pagination_class = CustomPagination
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    serializer_class = RecipeOnlyReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeOnlyReadSerializer
        return RecipeWriteSerializer

    def add_or_remove_object(self, request, pk, model, serializer, message):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        instance, created = model.objects.get_or_create(user=user,
                                                        recipe=recipe)

        if request.method == 'POST':
            if created:
                serializer = serializer(instance, context={'request': request})
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response({'errors': 'Рецепт уже добавлен.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            if created:
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self.add_or_remove_object(
            request,
            pk,
            Favorite,
            FavoriteSerializer,
            message={'errors': 'Нет рецепта в избранном!'}
        )

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self.add_or_remove_object(
            request,
            pk,
            ShoppingCart,
            ShoppingCartSerializer,
            message={'errors': 'Нет рецепта в списке покупок'}
        )

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = user.shopping_cart.all()

        if not shopping_cart.exists():
            return Response({'message': 'Список покупок пуст.'})

        ingredients = Ingredient.objects.filter(
            recipes__in=shopping_cart.values('recipe')
        ).values(
            'name',
            measurement=F('measurement_unit')
        ).annotate(
            total=Sum('ingredients_in_recipe__amount')).order_by('-total')

        shopping_list = []
        shopping_list.append('Список покупок:')

        for num, item in enumerate(ingredients, 1):
            shopping_list.append(f'{num}. {item["name"]} ('
                                 f'{item["measurement"]}) - {item["total"]}')

        response = HttpResponse('\n'.join(shopping_list),
                                content_type='text/plain')
        response['Content-Disposition'] = \
            f'attachment; filename={shopping_list}.txt'
        return response


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter
