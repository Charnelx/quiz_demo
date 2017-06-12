from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.contrib.auth import authenticate
from .forms import LoginForm, UserRegistrationForm


def user_login(request, *args, **kwargs):
    if request.user.is_authenticated():
        return redirect('home')
    else:
        form = LoginForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                login(request, *args, **kwargs)
                return redirect('home')
        return render(request, 'login.html', {'form':form})

def user_register(request, *args, **kwargs):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email = userObj['email']
            password = userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('/')
            else:
                form.add_error(None, 'Looks like a username with that email or password already exists')
                return render(request, 'register.html', {'form': form})
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})