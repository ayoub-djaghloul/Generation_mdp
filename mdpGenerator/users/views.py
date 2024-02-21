from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from .models import compte
# Create your views here.

def home(request):
    return render(request, 'users/home.html')

def login(request):
    return render(request, 'users/login.html')

def profile(request):
    user_accounts = compte.objects.filter(user=request.user)
    return render(request, 'users/profile.html', {'user_accounts': user_accounts})

def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account has been created!')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/signup.html', {'form': form})
