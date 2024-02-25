from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.login_signup, name='login_signup'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_view.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login_signup')), name='logout'),
]