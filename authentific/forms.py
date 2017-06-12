from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        required = True,
        label="Username",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder':'Username'}))
    password = forms.CharField(
        required=True,
        label="Password",
        max_length=30,
        widget=forms.TextInput(attrs={'type':'password', 'class': 'form-control', 'name': 'password', 'placeholder':'Password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache:
                return self.cleaned_data
            else:
                del self.cleaned_data['password']
                raise forms.ValidationError('User or password is incorrect.')

        return self.cleaned_data

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'Username',
        min_length = 3,
        max_length = 32,
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder':'Username'})
    )
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
        widget=forms.TextInput(attrs={'type':'email', 'class': 'form-control', 'name': 'username', 'placeholder':'email'})
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        min_length = 8,
        max_length = 32,
        widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', 'name': 'password', 'placeholder': 'Password'})
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if (username is not None) and (password) and (email):
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache:
                del self.cleaned_data['password']
                raise forms.ValidationError('User already exists')
            else:
                try:
                    User.objects.get(email=email)
                    raise forms.ValidationError('This email address is already in use.')
                except User.DoesNotExist:
                    pass

        return self.cleaned_data