from django_filters import rest_framework as filters
from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.CharFilter(
        field_name='tags__slug',
        lookup_expr='iexact'
    )
    is_favorited = filters.BooleanFilter(
        field_name='favorites',
        method='filter_added'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='shopping_cart',
        method='filter_added'
    )

    def filter_added(self, queryset, name, value):
        user = self.request.user
        if not value:
            return queryset
        if not user.is_authenticated:
            return queryset.none()
        lookup = '__'.join([name, 'user'])
        return queryset & Recipe.objects.filter(**{lookup: user})

    class Meta:
        model = Recipe
        fields = ('tags', 'author')
