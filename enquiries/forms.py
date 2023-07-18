from django import forms
from .models import Enquiry


class EnquiryStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ('is_contacted',)

        labels = {
            'is_contacted': 'has been contacted',
        }
