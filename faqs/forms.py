from dataclasses import field
import imp
from django import forms
from .models import Faq


class FaqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = ['question', 'answer', 'is_active']

        widgets = {
            'answer': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Answer', 'rows':'5'}),
            }
    
    def clean(self):
        data = self.cleaned_data
        question = data.get('question')
        qs = Faq.objects.filter(question__iexact=question)
        if qs.exists():
            self.add_error('question', f"The question, '{question}' has already exist.")
        return data


class FaqEditForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = ['question', 'answer', 'is_active']

        widgets = {
            'answer': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Answer', 'rows':'5'}),
            }