from drf_extra_fields.fields import Base64ImageField
from recipes.models import Recipe
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class UserReadSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')
        read_only_fields = ('id', 'is_subscribed')

    def get_is_subscribed(self, obj):
        if not self.context['request'].user.is_authenticated:
            return False
        return self.context['request'].user.subscriber.filter(
            subscribed=obj).exists()


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class PasswordChangeSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=128)
    old_password = serializers.CharField(source='password')

    class Meta:
        model = User
        fields = ('new_password', 'old_password')


class RecipeInfoSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribtionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField('get_limited_recipes')
    recipes_count = serializers.IntegerField(
        source='recipes.count'
    )

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes',
                  'recipes_count')
        read_only_fields = ('email', 'id', 'username', 'first_name',
                            'last_name', 'is_subscribed', 'recipes_count')

    def get_is_subscribed(self, obj):
        return self.context['request'].user.subscriber.filter(
            subscribed=obj).exists()

    def get_limited_recipes(self, obj):
        recipe_qs = obj.recipes.all()
        limit = self.context['request'].query_params.get('recipes_limit')
        try:
            limit = int(limit)
        except ValueError:
            raise ValidationError({
                'detail': 'recipes_limit должнен быть числом'})
        except TypeError:
            return RecipeInfoSerializer(instance=recipe_qs, many=True).data
        if limit < 0:
            raise ValidationError({
                'detail': 'recipes_limit не может быть отрицательным'})
        recipe_qs = recipe_qs[:int(limit)]
        return RecipeInfoSerializer(instance=recipe_qs, many=True).data


class SubscribtionCreateSerializer(SubscribtionSerializer):

    def get_is_subscribed(self, obj):
        return True
