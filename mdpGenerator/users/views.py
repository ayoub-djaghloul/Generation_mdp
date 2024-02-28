from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegisterForm
import random
import string
import nltk
from nltk.corpus import brown
# Create your views here.

nltk.download('brown')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

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

        # Generate password based on user input
        password = generateMdp(mode, n, special_characters, uppercase, numbers)

        # Pass the generated password to the template
        return render(request, 'users/passwordDisplay.html', {'password': password})

    # If not a POST request, or for the initial form load:
    return render(request, 'users/home.html')

def passwordDisplay(request):
    return render(request, 'users/passwordDisplay.html')
