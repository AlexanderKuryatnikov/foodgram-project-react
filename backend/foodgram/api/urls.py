from django.urls import include, path, re_path
from rest_framework import routers

from .views import (FavoriteAPIView, IngredientViewSet, RecipeViewSet,
                    ShoppingCartAPIView, TagViewSet,
                    download_shopping_cart_view)

router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet, basename='recipe')

urlpatterns = [
    re_path(
        r'recipes/(?P<id>\d+)/favorite/',
        FavoriteAPIView.as_view(),
        name='favorite'
    ),
    re_path(
        r'recipes/(?P<id>\d+)/shopping_cart/',
        ShoppingCartAPIView.as_view(),
        name='shopping_cart'
    ),
    path(
        'recipes/download_shopping_cart/',
        download_shopping_cart_view,
        name='download_shopping_cart'
    ),
    path('', include(router.urls)),
]
