from django import forms
from .models import Sale, Position


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('listing', 'commission')

        widgets = {
            'listing': forms.Select(attrs = {'class': 'form-select'}),
        }


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('position', 'buyer')

        widgets = {
            'position': forms.Select(attrs = {'class': 'form-select'}),
            'buyer': forms.Select(attrs = {'class': 'form-select'}),
        }


CHART_CHOICES = (
    ('#1', 'Bar Chart'),
    ('#2', 'Pie Chart'),
    ('#3', 'Line Chart'),
)

class SaleSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    chart_type = forms.ChoiceField(choices = CHART_CHOICES)


