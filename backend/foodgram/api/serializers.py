from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Ingridient, IngridientAmount, Recipe, Tag
from users.serializers import UserReadSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngridientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingridient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngridientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingridient.objects.all(),
        source='ingridient'
    )

    class Meta:
        model = IngridientAmount
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
    ingridients = RecipeIngridientSerializer(
        many=True,
        source='ingridient_amount'
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'ingridients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')
        read_only_fields = ('is_favorited', 'is_in_shopping_cart')

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
        ingridients_data = validated_data.pop('ingridient_amount')
        tag_data = validated_data.pop('tags')
        author = self.context['request'].user
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.ingridient_amount_create(recipe, tag_data, ingridients_data)
        return recipe

    def update(self, instance, validated_data):
        ingridients_data = validated_data.pop('ingridient_amount')
        tag_data = validated_data.pop('tags')
        Recipe.objects.filter(pk=instance.pk).update(**validated_data)
        IngridientAmount.objects.filter(recipe=instance).delete()
        self.ingridient_amount_create(instance, tag_data, ingridients_data)
        return instance

    def ingridient_amount_create(self, recipe, tag_data, ingridients_data):
        recipe.tags.set(tag_data)
        IngridientAmount.objects.bulk_create([
            IngridientAmount(recipe=recipe, **ingridient_data)
            for ingridient_data in ingridients_data
        ])
