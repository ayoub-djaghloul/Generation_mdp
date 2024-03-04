from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.http import JsonResponse
from django.utils.cache import add_never_cache_headers
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm
from .models import compte
from django.shortcuts import render, redirect

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

# Create your views here.
def login_signup(request):
    login_form = AuthenticationForm()
    signup_form = UserRegisterForm()

    if request.method == 'POST':
        if 'signup' in request.POST:  # Détecte l'action d'inscription
            signup_form = UserRegisterForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                username = user.username
                password = signup_form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                if user:
                    auth_login(request, user)
                    if is_ajax(request):
                        # Pour une requête AJAX, retourne une réponse JSON
                        return JsonResponse({"success": True, "message": "Hi {}, your account has been created!".format(username)})
                    else:
                        # Pour une requête non-AJAX, continuez avec la logique habituelle
                        messages.success(request, f'Hi {username}, your account has been created!')
                        return redirect('home')
                else:
                    print("User not authenticated")
            else:
                errors = signup_form.errors.as_json()
                if is_ajax(request):
                    return JsonResponse({"success": False, "errors": errors}, status=400)
                print(signup_form.errors)
        elif 'login' in request.POST:  # Détecte l'action de connexion
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                if is_ajax(request):
                    return JsonResponse({"success": True, "message": "You are now logged in!"})
                else:
                    messages.success(request, f'You are now logged in!')
                    return redirect('home')
            else:
                errors = login_form.errors.as_json()
                if is_ajax(request):
                    return JsonResponse({"success": False, "errors": errors}, status=400)
                print(login_form.errors)
    # Les formulaires sont passés au template, qu'ils aient été réinitialisés ou non
    response = render(request, 'users/login_signup.html', {'login_form': login_form, 'signup_form': signup_form})
    add_never_cache_headers(response)
    return response

@login_required(login_url='/')
def home(request):
    return render(request, 'users/home.html')

@login_required(login_url='/')
def profile(request):
    user_accounts = compte.objects.filter(user=request.user)
    return render(request, 'users/profile.html', {'user_accounts': user_accounts})


