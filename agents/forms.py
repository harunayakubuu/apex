from django import forms
from .models import Agent
from django.contrib.auth import get_user_model

User = get_user_model()


class AgencyAgentUserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')

        help_texts = {
                'username': None,
            }


class AgencyAgentUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_active', )

        # help_texts = {
        #         'username': None,
        #     }


class AgentCreateForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ('additional_phone_number', 'about', 'profile_picture', 'display_picture')

        # widgets = {
        #     'state': forms.Select(attrs = {'class': 'form-select'}),
        # }

class AgentUpdateForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ('additional_phone_number', 'about', 'profile_picture', 'display_picture')

        # widgets = {
        #     'state': forms.Select(attrs = {'class': 'form-select'}),
        # }