from django.contrib import admin
from .models import MoodQuestion, MoodOption

admin.site.register(MoodQuestion)
admin.site.register(MoodOption)