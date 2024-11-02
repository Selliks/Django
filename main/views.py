from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm


# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('web:secret')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def main_page(request):
    return render(request, "main_page.html")


def info(request):
    return render(request, "info.html")


def sign_up(request):
    return render(request, "sign_up.html")


def sign_in(request):
    return render(request, "sign_in.html")


@login_required
def secret_view(request):
    return render(request, "secret.html")
