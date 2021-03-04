from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import CommentViewSet, FollowAPIView, GroupAPIView, PostViewSet

API_VERSION = 'v1/'

router_v1 = DefaultRouter()

router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register(
    r'posts\/(?P<post_id>\d+)\/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path(
        API_VERSION + 'token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        API_VERSION + 'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'),
    path(API_VERSION + 'follow/', FollowAPIView.as_view(), name='follow'),
    path(API_VERSION + 'group/', GroupAPIView.as_view(), name='group'),
    path(API_VERSION, include(router_v1.urls)),
]
