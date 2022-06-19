import csv

from django.db import IntegrityError
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from rest_framework import mixins, status, views, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.paginators import CustomPagination
from users.serializers import RecipeInfoSerializer

from .filters import IngredientFilter, RecipeFilter
from .permissions import AuthorOrAuthPostOrReadOnly
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


class ListRetrieveViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AuthorOrAuthPostOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter


class FavoriteAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, **kwargs):
        recipe_id = kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        user = request.user
        try:
            Favorite.objects.create(user=user, recipe=recipe)
        except IntegrityError:
            raise ValidationError({'detail': 'Рецепт уже есть в избранном'})
        serializer = RecipeInfoSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        recipe_id = kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        user = request.user
        instance = Favorite.objects.filter(user=user,
                                           recipe=recipe)
        if not instance:
            raise ValidationError(
                {'detail': 'Рецепта нет в избранном'})
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, **kwargs):
        recipe_id = kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        user = request.user
        try:
            ShoppingCart.objects.create(user=user, recipe=recipe)
        except IntegrityError:
            raise ValidationError({'detail': 'Рецепт уже есть в покупках'})
        serializer = RecipeInfoSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        recipe_id = kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        user = request.user
        instance = ShoppingCart.objects.filter(user=user,
                                               recipe=recipe)
        if not instance:
            raise ValidationError(
                {'detail': 'Рецепта нет в покупках'})
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_shopping_cart_view(request):
    shopping_cart = request.user.shopping_cart.all()
    in_cart = Recipe.objects.filter(shopping_cart__in=shopping_cart)
    shopping_list = (
        IngredientAmount.objects
        .values('ingredient__name', 'ingredient__measurement_unit')
        .filter(recipe__in=in_cart)
        .annotate(amount=Sum('amount'))
    )
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        'attachment;filename="shopping_list.csv"'
    )
    writer = csv.writer(response)
    for row in shopping_list:
        writer.writerow([row['ingredient__name'],
                         row['amount'],
                         row['ingredient__measurement_unit']])
    return response
