from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', views.password_generator_view, name='home'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('passwordDisplay/', views.passwordDisplay, name='display_password'),
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('', auth_views.LogoutView.as_view(template_name='users/login.html'), name='logout'),
    path('save_password/', views.save_password, name='save_password'),
]
