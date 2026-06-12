from django.urls import path
from . import views

urlpatterns = [
    path('create_post/', views.create_post, name='create_post'),
    path('edit_post/',views.edit_post,name='edit_post'),
    path('feed/', views.feed, name='feed'),
]