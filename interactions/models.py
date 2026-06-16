from django.db import models
from django.conf import settings


class StoryChain(models.Model):

    title = models.CharField(
        max_length=200
    )

    starter_content = models.TextField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    is_completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class StoryContribution(models.Model):

    story = models.ForeignKey(
        StoryChain,
        on_delete=models.CASCADE,
        related_name='contributions'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.story.title}"