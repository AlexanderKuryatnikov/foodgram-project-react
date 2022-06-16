from django.contrib import admin

from .models import (Favorite, Ingridient, IngridientAmount, Recipe,
                     ShoppingCart, Tag)


class IngridientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')


class IngridientAmountInline(admin.TabularInline):
    model = IngridientAmount
    extra = 1
    list_display = ('pk', 'ingridient', 'recipe', 'amount')


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngridientAmountInline,)
    readonly_fields = ('times_favorited',)
    list_display = ('pk', 'name', 'author', 'pub_date', 'get_tags')
    search_fields = ('name', 'author__username', 'tags__name')

    def get_tags(self, obj):
        return '\n'.join([tag.name for tag in obj.tags.all()])

    def times_favorited(self, obj):
        return obj.favorites.all().count()


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user')
    search_fields = ('user__username',)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user')
    search_fields = ('user__username',)


admin.site.register(Ingridient, IngridientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
