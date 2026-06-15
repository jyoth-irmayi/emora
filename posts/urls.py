from django.urls import path
from . import views

urlpatterns = [
    path('create_post/', views.create_post, name='create_post'),
    path('<int:post_id>/edit/', views.edit_post, name='edit-post'),
    path('feed/', views.feed, name='feed'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('comment_post/<int:post_id>/', views.comment_post, name='comment_post'),
    path('delete_comment/<int:id>/', views.delete_comment, name='delete_comment'),
    path('<int:post_id>/save_post/', views.save_post, name='save-post'),
    path('<int:post_id>/delete/', views.delete_post, name='delete-post'),
]   