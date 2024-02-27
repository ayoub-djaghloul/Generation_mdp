from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegisterForm
# Create your views here.

@login_required()
def home(request):
    return render(request, 'users/home.html')

@login_required()
def profile(request):
    return render(request, 'users/profile.html')

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

def passwordDisplay(request):
    return render(request, 'users/passwordDisplay.html')
