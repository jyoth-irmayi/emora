from django.urls import path
from . import views

urlpatterns = [
    path('create_post/', views.create_post, name='create_post'),
    path('edit_post/',views.edit_post,name='edit_post'),
    path('feed/', views.feed, name='feed'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('comment_post/<int:post_id>/', views.comment_post, name='comment_post'),
    path('delete_comment/<int:id>/', views.delete_comment, name='delete_comment'),
]   