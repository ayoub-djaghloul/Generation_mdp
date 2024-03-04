from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.login_signup, name='login_signup'),
    path('profile/', views.profile, name='profile'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login_signup')), name='logout'),

    path('home/', views.password_generator_view, name='home'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('passwordDisplay/', views.passwordDisplay, name='display_password'),
    path('', auth_view.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('save_password/', views.save_password, name='save_password'),
    path('passwordDisplay/', views.passwordDisplay, name='passwordDisplay'),
]