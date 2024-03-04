import string
from random import random

import brown as brown
import nltk as nltk
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
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
# Create your views here.

@login_required()
def home(request):
    return render(request, 'users/home.html')

@login_required()
def profile(request):
    user_accounts = compte.objects.filter(user=request.user)
    return render(request, 'users/profile.html', {'user_accounts': user_accounts})


    return render(request, 'users/signup.html', {'form': form})


def generateMdpRand(n, caractereSpeciaux, maj, nbr):
    caracteres = string.ascii_lowercase

    if maj:
        caracteres += string.ascii_uppercase
    if nbr:
        caracteres += string.digits
    if caractereSpeciaux:
        caracteres += string.punctuation

    password_parts = []
    if maj:
        password_parts.append(random.choice(string.ascii_uppercase))
    if nbr:
        password_parts.append(random.choice(string.digits))
    if caractereSpeciaux:
        password_parts.append(random.choice(string.punctuation))

    remaining_length = n - len(password_parts)
    password_parts += random.choices(caracteres, k=remaining_length)

    random.shuffle(password_parts)

    password = ''.join(password_parts)

    return password


def fetch_random_words_from_nltk_corpus(n, corpus_name='brown'):
    """Sélectionne n mots aléatoires à partir d'un corpus NLTK spécifié."""
    if corpus_name == 'brown':
        corpus = brown
    else:
        corpus = brown
    words = list(set(corpus.words()))
    random_words = random.sample(words, n)
    return random_words


def generate_basic_sentence(n):
    """Génère une phrase simple en sélectionnant des mots de manière aléatoire."""
    while True:
        words = fetch_random_words_from_nltk_corpus(n, 'brown')
        tagged_words = nltk.pos_tag(words)

        noun = [word for word, tag in tagged_words if tag.startswith('NN')]
        verb = [word for word, tag in tagged_words if tag.startswith('VB')]
        adj = [word for word, tag in tagged_words if tag.startswith('JJ')]

        if noun and verb and adj:
            return f"The {adj[0]} {noun[0]} {verb[0]}"


def generateMdpWord(n, caractereSpeciaux, maj, nbr):
    words = generate_basic_sentence(n).split()

    if not (caractereSpeciaux or maj or nbr):
        return ' '.join(words)

    password_parts = []
    for word in words:
        password_parts.append(word)
        if caractereSpeciaux:
            password_parts.append(random.choice(string.punctuation))
        if nbr:
            password_parts.append(str(random.randint(0, 9)))

    if not caractereSpeciaux and not nbr:
        password = ' '.join(password_parts)
    else:
        password = ''.join(password_parts)

    if maj:
        letters_indices = [i for i, c in enumerate(password) if c.isalpha()]
        n_maj = len(letters_indices) // 4
        indices_to_capitalize = random.sample(letters_indices, n_maj)
        password_chars = list(password)
        for i in indices_to_capitalize:
            password_chars[i] = password_chars[i].upper()
        password = ''.join(password_chars)

    return password

def generateMdp(mode, n, caractereSpeciaux, maj, nbr):
    if mode == 0:
        return generateMdpWord(n, caractereSpeciaux, maj, nbr)
    elif mode == 1:
        return generateMdpRand(n, caractereSpeciaux, maj, nbr)

def password_generator_view(request):
    if request.method == "POST":
        mode = int(request.POST.get("mode", 1))  # Default to Random based generation if not specified
        n = int(request.POST.get("n", 8))  # Default length
        special_characters = "specialcharacter" in request.POST
        uppercase = "uppercase" in request.POST
        numbers = "numbers" in request.POST

        password = generateMdp(mode, n, special_characters, uppercase, numbers)

        return render(request, 'users/passwordDisplay.html', {'password': password})

    return render(request, 'users/home.html')

def passwordDisplay(request):
    return render(request, 'users/passwordDisplay.html')

@login_required()
def save_password(request):
    if request.method == 'POST':
        platform = request.POST.get('platform')
        password = request.POST.get('password')
        user = request.user

        new_compte = compte(user=user, platform=platform, password=password)
        new_compte.save()
        messages.success(request, 'Password saved successfully!')


        return HttpResponseRedirect(reverse('home'))

    return HttpResponseRedirect(reverse('home'))
