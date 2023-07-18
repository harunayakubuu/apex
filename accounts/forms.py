from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from .models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
        field_classes = {'username': UsernameField}

        # widgets = {
        #     'username': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Username'}),
        #     'email': forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Email Address'}),
        #     'password1': forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Password'}),
        #     'password2': forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Password Confirmation'}),
        # }

        help_texts = {
            'username': None,
        }

    # def clean(self):
    #     data = self.cleaned_data
    #     username = data.get('username')
    #     if len(username) < 6:
    #         self.add_error('username', f"Username must be six or more characters long.")
    #     return data


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'phone_number']

    # def clean(self):
    #     data = self.cleaned_data
    #     username = data.get('username')
    #     if len(username) < 6:
    #         self.add_error('username', f"Username must be six or more characters long.")
    #     return data