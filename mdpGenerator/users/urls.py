from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [

    path('home/', views.password_generator_view, name='home'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('passwordDisplay/', views.passwordDisplay, name='display_password'),
    path('', auth_view.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('save_password/', views.save_password, name='save_password'),

]