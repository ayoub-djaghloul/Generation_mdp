from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .forms import UserRegisterForm
from .models import compte
import random
import string
from transformers import pipeline
import re
import random
import string

from nltk.corpus import brown
# Create your views here.

@login_required()
def home(request):
    return render(request, 'users/home.html')

@login_required()
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

def generate_sentence_gpt2(n):
    generator = pipeline('text-generation', model="gpt2", device=0)

    prompt = ""
    outputs = generator(prompt, max_length=n+(n*3), num_return_sequences=1, pad_token_id=50256)

    generated_text = outputs[0]["generated_text"].strip()

    words = re.findall(r'\b[a-zA-Z]{2,}\b', generated_text)

    adjusted_sentence = ' '.join(words[:n])

    adjusted_sentence = adjusted_sentence.lower()

    return adjusted_sentence




def generate_and_evaluate_sentence_gpt2(n, confidence_threshold=0.92, max_attempts=3):

    generator = pipeline('text-generation', model="gpt2", device=0)
    sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", device=0)

    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        outputs = generator("", max_length=n+(n*3), num_return_sequences=1, pad_token_id=50256)
        generated_text = outputs[0]["generated_text"].strip()
        words = re.findall(r'\b[a-zA-Z]{2,}\b', generated_text)
        adjusted_sentence = ' '.join(words[:n]).lower()

        # Évaluation du sentiment de la phrase ajustée
        sentiment_result = sentiment_analyzer(adjusted_sentence)[0]
        confidence = sentiment_result['score']

        # Si le taux de confiance dépasse le seuil, retourne la phrase
        if confidence > confidence_threshold:
            return adjusted_sentence

    # Si toutes les tentatives échouent, retourne li jat
    return adjusted_sentence


def generateMdpWord(n, caractereSpeciaux, maj, nbr):
    words = generate_and_evaluate_sentence_gpt2(n).split()

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


def generateMdpRandWithScore(score):
    caractereSpeciaux = False
    maj = False
    nbr = False
    if score <= 10:
        length = 4
    elif score <= 25:
        length = 8
    elif score <= 50:
        length = 10
    elif score <= 75:
        length = 12
    else:
        length = 16

    caractereSpeciaux = score > 50
    maj = score > 25
    nbr = score > 25

    return generateMdpRand(length, caractereSpeciaux, maj, nbr)


def generateMdpWordWithScore(score):
    caractereSpeciaux = False
    maj = False
    nbr = False

    if score <= 25:
        num_words = 2
    elif score <= 50:
        num_words = 3
    elif score <= 75:
        num_words = 3
    else:
        num_words = 4

    caractereSpeciaux = score > 50
    maj = score > 25
    nbr = score > 25

    return generateMdpWord(num_words, caractereSpeciaux, maj, nbr)


def generateMdp(mode, n, caractereSpeciaux, maj, nbr):
    if mode == 0:
        return generateMdpWord(n, caractereSpeciaux, maj, nbr)
    elif mode == 1:
        return generateMdpRand(n, caractereSpeciaux, maj, nbr)
    elif mode ==2:
        return generateMdpWordWithScore(n)
    elif mode ==3:
       return generateMdpRandWithScore(n)
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