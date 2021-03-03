from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, permissions, viewsets

from .models import Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        save_params = {
            'author': self.request.user,
            'post_id': self.kwargs.get('post_id')
        }
        serializer.save(**save_params)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        all_comments_of_post = post.comments.all()
        return all_comments_of_post


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
            'user': get_object_or_404(
                User, username=self.request.user),
            'following': get_object_or_404(
                User, username=self.request.data.get('following'))
        }
        serializer.save(**save_params)


class GroupAPIView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer

    def get_queryset(self):
        groups = Group.objects.all()
        return groups
