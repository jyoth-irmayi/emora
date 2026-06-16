from django.contrib import admin
from .models import StoryChain, StoryContribution

# Register your models here.
admin.site.register(StoryChain)
admin.site.register(StoryContribution)