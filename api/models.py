from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField('название группы', max_length=200)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey(
        Group, models.SET_NULL, blank=True,
        null=True, related_name='posts', verbose_name='группа',
        help_text='Выберите группу для публикации поста.')

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='follower', verbose_name='подписчик')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following', verbose_name='автор')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='following_unique',),
        ]
