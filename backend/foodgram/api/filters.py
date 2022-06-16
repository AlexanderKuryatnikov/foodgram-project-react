from django_filters import rest_framework as filters

from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    CHOICES = (
        (0, 'all'),
        (1, 'added_only')
    )
    tags = filters.CharFilter(
        field_name='tags__slug',
        lookup_expr='iexact'
    )
    is_favorited = filters.ChoiceFilter(
        choices=CHOICES,
        field_name='favorites',
        method='filter_added'
    )
    is_in_shopping_cart = filters.ChoiceFilter(
        choices=CHOICES,
        field_name='shopping_cart',
        method='filter_added'
    )

    def filter_added(self, queryset, name, value):
        user = self.request.user
        if value == '0':
            return queryset
        if not user.is_authenticated:
            return queryset.none()
        lookup = '__'.join([name, 'user'])
        return queryset & Recipe.objects.filter(**{lookup: user})

    class Meta:
        model = Recipe
        fields = ('tags', 'author')
