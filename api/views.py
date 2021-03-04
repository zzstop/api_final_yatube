from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, viewsets

from .models import Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('group',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        all_comments_of_post = post.comments.all()
        return all_comments_of_post

    def perform_create(self, serializer):
        save_params = {
            'author': self.request.user,
            'post_id': self.kwargs.get('post_id')
        }
        serializer.save(**save_params)


class FollowAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username',)

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        user_followers = user.following.all()
        return user_followers

    def perform_create(self, serializer):
        save_params = {
            'user': self.request.user,
            'following': User.objects.get(
                username=self.request.data.get('following'))
        }
        serializer.save(**save_params)


class GroupAPIView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
