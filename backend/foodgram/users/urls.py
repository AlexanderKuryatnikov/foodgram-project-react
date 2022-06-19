from django.urls import include, path, re_path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework import routers

from .views import (SubscribtionAPIView, SubscribtionListView, UserSelfView,
                    UserViewSet, password_change_view)

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path(
        'auth/token/login/',
        TokenCreateView.as_view(),
        name='token-create'
    ),
    path(
        'auth/token/logout/',
        TokenDestroyView.as_view(),
        name='token-destoy'
    ),
    path(
        'users/set_password/',
        password_change_view,
        name='set-password'
    ),
    path(
        'users/me/',
        UserSelfView.as_view(),
        name='user-me'
    ),
    path(
        'users/subscribtions/',
        SubscribtionListView.as_view(),
        name='subscribtions'
    ),
    re_path(
        r'users/(?P<id>\d+)/subscribe/',
        SubscribtionAPIView.as_view(),
        name='subscribe'
    ),
    path('', include(router.urls)),
]
