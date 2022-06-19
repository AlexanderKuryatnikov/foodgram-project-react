from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, IngredientAmount, Recipe, Tag
from rest_framework import serializers
from users.serializers import UserReadSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    author = UserReadSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    ingredients = RecipeIngredientSerializer(
        many=True,
        source='ingredient_amount'
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')
        read_only_fields = ('id', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.favorites.filter(user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.shopping_cart.filter(user=user).exists()

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredient_amount')
        tag_data = validated_data.pop('tags')
        author = self.context['request'].user
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.ingridient_amount_create(recipe, tag_data, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredient_amount')
        tag_data = validated_data.pop('tags')
        Recipe.objects.filter(pk=instance.pk).update(**validated_data)
        IngredientAmount.objects.filter(recipe=instance).delete()
        self.ingridient_amount_create(instance, tag_data, ingredients_data)
        return instance

    def ingridient_amount_create(self, recipe, tag_data, ingredients_data):
        recipe.tags.set(tag_data)
        IngredientAmount.objects.bulk_create([
            IngredientAmount(recipe=recipe, **ingredient_data)
            for ingredient_data in ingredients_data
        ])
