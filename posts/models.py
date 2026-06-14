from django.db import models
from django.conf import settings

class Post(models.Model):

    POST_TYPES = (
        ('quote', 'Quote'),
        ('poem', 'Poem'),
        ('story', 'Story'),
    )

    MOODS = (
        ('healing', 'Healing'),
        ('sad', 'Sad'),
        ('motivated', 'Motivated'),
        ('calm', 'Calm'),
        ('lonely', 'Lonely'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    post_type = models.CharField(
        max_length=10,
        choices=POST_TYPES
    )

    title = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    content = models.TextField()

    mood = models.CharField(
        max_length=20,
        choices=MOODS
    )

    background = models.CharField(
        max_length=20,
        default='bg1'
    )

    is_anonymous = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.post_type} - {self.user.username}"
    


class Like(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.user.username} - {self.post.id}'