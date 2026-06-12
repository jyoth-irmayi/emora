from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    bio = models.TextField(blank=True,null=True)
    avatar_color = models.CharField(max_length=20, default="#4f46e5")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_initials(self):

        name = self.username
        words = name.split()

        if len(words) == 1:
            return words[0][:2].upper()

        return (words[0][0] + words[1][0]).upper()