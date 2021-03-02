from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post
from .serializers import CommentSerializer, PostSerializer

PERMISSION_CLASSES = (IsAuthenticatedOrReadOnly,)


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = PERMISSION_CLASSES
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = PERMISSION_CLASSES
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
