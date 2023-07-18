from django import forms
from .models import PrivacyPolicy, Service, TermsAndCondition#AboutUs


# class AboutUsForm(forms.ModelForm):
#     class Meta:
#         model = AboutUs
#         fields = ['about']

        # widgets = {
        #     'policy': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Policy', 'rows':'4'}),
        #     }

class PrivacyPolicyForm(forms.ModelForm):
    class Meta:
        model = PrivacyPolicy
        fields = ['title', 'policy', 'is_active']

        widgets = {
            'policy': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Policy', 'rows':'4'}),
            }
    

class PrivacyPolicyEditForm(forms.ModelForm):
    class Meta:
        model = PrivacyPolicy
        fields = ['title', 'policy', 'is_active']

        widgets = {
            'policy': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Policy', 'rows':'4'}),
            }


class TermsAndConditionForm(forms.ModelForm):
    class Meta:
        model = TermsAndCondition
        fields = ['term', 'condition', 'is_active']

        widgets = {
            'condition': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'', 'rows':'4'}),
            }
    

class TermsAndConditionEditForm(forms.ModelForm):
    class Meta:
        model = TermsAndCondition
        fields = ['term', 'condition', 'is_active']

        widgets = {
            'condition': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'', 'rows':'4'}),
            }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'is_active']

        widgets = {
            'condition': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'', 'rows':'4'}),
            }
    

class ServiceEditForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'is_active']

        widgets = {
            'condition': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'', 'rows':'4'}),
            }