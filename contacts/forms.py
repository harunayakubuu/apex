from django import forms
from django.contrib.auth import get_user_model

from .models import Contact, EmergencyContact


User = get_user_model()


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'phone', 'message']

        widgets = {
            'name': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Name'}),
            'phone': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Phone number'}),
            'email': forms.EmailInput(attrs = {'class': 'form-control', 'placeholder':'Email (Optional)'}),
            'subject': forms.Select(attrs = {'class': 'form-select', 'placeholder':'Select subject'}),
            'message': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Message', 'rows':'5'}),
            }


class ContactUpdateForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['status',]


class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = (
            'full_name', 
            'relationship', 
            'email',
            'phone', 
            'address', 
            'state', 
            'comment', 
            'picture', 
            'next_of_kin'
            )
        widgets = {
            'relationship': forms.Select(attrs = {'class': 'form-select', 'placeholder':'Select subject'}),
            'state': forms.Select(attrs = {'class': 'form-select', 'placeholder':'Select State'}),
            'comment': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Comment', 'rows':'4'}),
        }