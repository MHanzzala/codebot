from django.shortcuts import render, redirect
from django.contrib import messages
import openai
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm

# Create your views here.


def home(request):
    lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'go', 'html', 'java', 'javascript', 'markup', 'markup-templating', 'matlab',
                 'mongodb', 'objectivec', 'perl', 'php', 'powershell', 'python', 'r', 'regex', 'ruby', 'rust', 'sass', 'scala', 'sql', 'swift', 'yaml']

    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']

        # Check to make sure they picked a lang
        if lang == "Select your Programming Language":
            messages.success(
                request, "Hey! You Forgot To Pick A Programming Language...")
            return render(request, 'home.html', {'lang_list': lang_list, 'response': code, 'code': code, 'lang': lang})
        else:
            # OpenAI Key
            openai.api_key = "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"
            # Create OpenAI Instance
            openai.Model.list()
            # Make an OpenAI Request
            try:
                response = openai.Completion.create(
                    engine='text-davinci-003',
                    prompt=f"Respond only with code. Fix this {lang} code: {code}",
                    temperature=0,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                )
                # parse the response
                response = (response["choices"][0]["text"]).strip()
                return render(request, 'home.html', {'lang_list': lang_list, 'response': response, 'lang': lang})

            except Exception as e:
                return render(request, 'home.html', {'lang_list': lang_list, 'response': e, 'lang': lang})

    return render(request, 'home.html', {'lang_list': lang_list})


def suggest(request):
    lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'go', 'html', 'java', 'javascript', 'markup', 'markup-templating', 'matlab',
                 'mongodb', 'objectivec', 'perl', 'php', 'powershell', 'python', 'r', 'regex', 'ruby', 'rust', 'sass', 'scala', 'sql', 'swift', 'yaml']

    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']

        # Check to make sure they picked a lang
        if lang == "Select your Programming Language":
            messages.success(
                request, "Hey! You Forgot To Pick A Programming Language...")
            return render(request, 'suggest.html', {'lang_list': lang_list, 'response': code, 'code': code, 'lang': lang})
        else:
            # OpenAI Key
            openai.api_key = "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"
            # Create OpenAI Instance
            openai.Model.list()
            # Make an OpenAI Request
            try:
                response = openai.Completion.create(
                    engine='text-davinci-003',
                    prompt=f"Respond only with code. {code}",
                    temperature=0,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                )
                # parse the response
                response = (response["choices"][0]["text"]).strip()
                return render(request, 'suggest.html', {'lang_list': lang_list, 'response': response, 'lang': lang})

            except Exception as e:
                return render(request, 'suggest.html', {'lang_list': lang_list, 'response': e, 'lang': lang})

    return render(request, 'suggest.html', {'lang_list': lang_list})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been successfully logged in")
            return redirect('home')
        else:
            messages.success(request, "Error Logging in. Please try again!")
            return redirect('home')
    else:
        return render(request, "home.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect('home')


def register_user(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You have been registered successfully.")
			return redirect('home')

	else:
		form = SignUpForm()

	return render(request, 'register.html', {"form": form})
