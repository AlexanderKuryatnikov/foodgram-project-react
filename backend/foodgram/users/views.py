from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status, views, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Subscribtion, User
from .paginators import CustomPagination
from .serializers import (PasswordChangeSerializer,
                          SubscribtionCreateSerializer, SubscribtionSerializer,
                          UserReadSerializer, UserRegisterSerializer)


class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                  mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        return UserReadSerializer


class UserSelfView(generics.RetrieveAPIView):
    serializer_class = UserReadSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def password_change_view(request):
    serializer = PasswordChangeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = request.user

    if not user.check_password(serializer.validated_data.get('password')):
        raise ValidationError({'old_password': 'Неправильный старый пароль'})
    if (serializer.validated_data.get('password')
            == serializer.validated_data.get('new_password')):
        raise ValidationError(
            {'detail': 'Новый пароль должен отличаться от старого'}
        )

    user.set_password(serializer.validated_data.get('new_password'))
    user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribtionListView(generics.ListAPIView):
    serializer_class = SubscribtionSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        return User.objects.filter(subscribed__user=self.request.user)


class SubscribtionAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        subscriber = request.user
        subscribed = get_object_or_404(User, pk=user_id)
        if subscriber == subscribed:
            raise ValidationError(
                {'detail': 'Нельзя подписаться на себя самого'})
        try:
            Subscribtion.objects.create(user=subscriber, subscribed=subscribed)
        except IntegrityError:
            raise ValidationError(
                {'detail': 'Вы уже подписаны на этого пользователя'})
        serializer = SubscribtionCreateSerializer(subscribed,
                                                  context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        subscriber = request.user
        subscribed = get_object_or_404(User, pk=user_id)
        instance = Subscribtion.objects.filter(user=subscriber,
                                               subscribed=subscribed)
        if not instance:
            raise ValidationError(
                {'detail': 'Вы не подписаны на этого пользователя'})
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
