from rest_framework import serializers

from .models import Comment, Follow, Group, Post


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('title',)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    group = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ('id', 'group', 'text', 'author', 'pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created',)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    following = serializers.ReadOnlyField(source='following.username')

    class Meta:
        model = Follow
        fields = ('user', 'following',)
