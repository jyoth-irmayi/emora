from django.urls import path
from . import views

urlpatterns = [
    path('mood_test/', views.mood_test, name='mood_test'),
    path('music/', views.recommended_music, name='recommemded_music'),
]