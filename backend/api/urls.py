from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import RecipeViewSet, TagViewSet, IngredientViewSet

app_name = 'api'

router = DefaultRouter()
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
