from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('resend_otp/',views.resend_otp,name='resend_otp'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('logout/',views.logout_view,name='logout'),
    path('profile/', views.profile, name='profile'),
    path('post_detail/<int:id>/', views.post_detail, name='post_detail'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]