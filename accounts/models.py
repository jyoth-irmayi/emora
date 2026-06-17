from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import random
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
    

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)