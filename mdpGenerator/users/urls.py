from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('', auth_view.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),

]