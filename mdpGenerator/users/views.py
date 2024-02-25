from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.utils.cache import add_never_cache_headers
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm
from .models import compte
from django.shortcuts import render, redirect
# Create your views here.
def login_signup(request):
    # Initialiser les formulaires ici pour s'assurer qu'ils sont toujours définis
    login_form = AuthenticationForm()
    signup_form = UserRegisterForm()

    if request.method == 'POST':
        if 'signup' in request.POST:
            signup_form = UserRegisterForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()  # This saves the user and returns the user instance
                username = user.username  # Directly use the username from the user instance
                password = signup_form.cleaned_data['password1']  # Get the password to authenticate
                user = authenticate(username=username, password=password)  # Authenticate the user
                if user:
                    auth_login(request, user)  # Log the user in
                    messages.success(request, f'Hi {username}, your account has been created!')
                    return redirect('home')
                else:
                    print("User not authenticated")
            else:
                print(signup_form.errors)  # Affiche les erreurs de validation du formulaire
        else:
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                return redirect('home')

    # Les formulaires sont passés au template, qu'ils aient été réinitialisés ou non
    response = render(request, 'users/login_signup.html', {'login_form': login_form, 'signup_form': signup_form})
    add_never_cache_headers(response)
    return response
@login_required(login_url='/')
def home(request):
    return render(request, 'users/home.html')

def login(request):
    return render(request, 'users/login.html')
@login_required(login_url='/')
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
