from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from .models import Post
from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, FollowSerializer, PostSerializer

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        save_params = {
            'author': self.request.user,
            'post_id': self.kwargs.get('post_id', '')
        }
        serializer.save(**save_params)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id', '')
        post = get_object_or_404(Post, pk=post_id)
        all_comments_of_post = post.comments.all()
        return all_comments_of_post


class FollowAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowSerializer

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        user_followers = user.following.all()
        return user_followers

    def perform_create(self, serializer):
        user = get_object_or_404(User, username=self.request.user)
        following = self.request.data.get('following', '')
        following = get_object_or_404(User, username=following)
        if user == following:
            return serializer.errors
        serializer.save(user=user, following=following)
