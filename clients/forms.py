from django import forms
from .models import Client, Customer
from datetime import datetime

from django.contrib.auth import get_user_model
User = get_user_model()


# class AgencyAgentUserCreateForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('email', 'username', 'first_name', 'last_name')


class AdminClientUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_active', )


class ClientCreateForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('m', "Male"),
        ('f', "Female"),
    )
    gender = forms.ChoiceField(choices= GENDER_CHOICES, widget = forms.RadioSelect())
    class Meta:
        model = Client
        fields = ('state', 'home_address', 'business_address', 'gender', 'profile_picture')
        
        widgets = {
            'state': forms.Select(attrs = {'class': 'form-select'}),
        }


class ClientUpdateForm(forms.ModelForm):
    # GENDER_CHOICES = (
    #     ('m', "Male"),
    #     ('f', "Female"),
    # )
    # gender = forms.ChoiceField(choices= GENDER_CHOICES, widget = forms.RadioSelect())
    
    class Meta:
        model = Client
        fields = ('state', 'home_address', 'business_address', 'profile_picture')# 'gender', )#, 'dob')

        widgets = {
            'state': forms.Select(attrs = {'class': 'form-select'}),
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'middle_name', 'last_name', 'phone_number', 'email', 'state', 'local_government_area', 'home_address', 'business_address', 'gender', 'identification', 'picture')
        
        widgets = {
            'state': forms.Select(attrs = {'class': 'form-select'}),
            'gender': forms.Select(attrs = {'class': 'form-select'}),
        }