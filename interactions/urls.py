from django.urls import path
from . import views

urlpatterns = [
    path('create_story_chain/', views.create_story_chain, name ='create_story_chain'),
    path('continue_story/<int:story_id>/', views.continue_story, name ='continue_story'),
    path('story/<int:pk>/', views.story_detail, name='story_detail'),

]