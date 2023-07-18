from django import forms
from django.forms.models import modelformset_factory
from django.forms import inlineformset_factory
from .models import(
    Listing,
    ListingNearby,
    ListingPicture,
    ListingVideo,
    ListingSpecification,
    ListingType,
)
from agents.models import Agent


class ListingCreateForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['name', 'description', 'address', 'category', 'price', 'price_status', 'status', 'listing_type', 'location', 'city', 'state', 'length', 'breadth', 'encumbrances', 'encumbrance_description']

        labels = {
            'name': 'Property Name',
            'category': 'Property Category',
            'listing_type': 'Property Type',
            'description': 'Property Description'
            # 'description': 'Property Description'
        }
        
        widgets = {
            'name': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Property name'}),
            'description': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Property description', 'rows':'4'}),
            'category': forms.Select(attrs = {'class': 'form-select'}),
            'listing_type': forms.Select(attrs = {'class': 'form-select'}),
            'price_status': forms.Select(attrs = {'class': 'form-select'}),
            'status': forms.Select(attrs = {'class': 'form-select'}),
            'state': forms.Select(attrs = {'class': 'form-select'}),
            
            # 'category': forms.CheckboxSelectMultiple(attrs = {'class': 'form-control'}),
            'address': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Full address. E.g No. C250, ABC Road'}),
        }
        
    def clean(self):
        data = self.cleaned_data
        address = data.get('address')
        qs = Listing.objects.filter(address__iexact=address)
        if qs.exists():
            self.add_error('address', f"Another property with the same address, '{address}' has already been submitted. Please check and make update.")
        return data

    # def __init__(self, category, *args, **kwargs):
    #     super(ListingCreateForm, self).__init__(category, *args, **kwargs)
    #     self.fields['listing_type'].queryset = ListingType.objects.filter(category=category)


class ListingUpdateForm(forms.ModelForm):
    # listing_agent = forms.ModelChoiceField(queryset = Agent.objects.filter(organization.id == request.user.profile.id))
    # listing_agent = forms.ModelChoiceField(queryset = Agent.objects.filter(organization=request.user.profile))
    class Meta:
        model = Listing        
        fields = [
            'name',
            'listing_agent',
            'category',
            'listing_type',
            'price',
            'price_status',
            'status',
            'address',
            'location',
            'city', 
            'state',
            'length',
            'breadth',
            'description',
            'withdraw',
            ]
        
        labels = {
            'name': 'Property Name',
            'listing_agent': 'Property Agent',
            'category': 'Property Category',
            'listing_type': 'Property Type',
            'description': 'Property Description'
        }

        widgets = {
            'name': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Property name'}),
            'listing_agent': forms.Select(attrs = {'class': 'form-select'}),
            'description': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Property description', 'rows':'4'}),
            'category': forms.Select(attrs = {'class': 'form-select'}),
            'listing_type': forms.Select(attrs = {'class': 'form-select'}),
            'price_status': forms.Select(attrs = {'class': 'form-select'}),
            'status': forms.Select(attrs = {'class': 'form-select'}),
            'state': forms.Select(attrs = {'class': 'form-select'}),
            
            # 'category': forms.CheckboxSelectMultiple(attrs = {'class': 'form-control'}),
            'address': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Full address. E.g No. C250, ABC Road'}),
        }

class ListingSpecificationForm(forms.ModelForm):
    class Meta:
        model = ListingSpecification
        fields = ['attribute', 'value']


ListingSpecificationFormset = modelformset_factory(
    ListingSpecification,
    form = ListingSpecificationForm,
    extra = 0
)


class ListingVideoForm(forms.ModelForm):
    class Meta:
        model = ListingVideo
        fields = ['video']


class ListingPictureForm(forms.ModelForm):
    class Meta:
        model = ListingPicture
        fields = ['name', 'picture', 'is_feature']

        widgets = {
            'name': forms.TextInput(attrs={"class":"form-control"}),
            'picture': forms.FileInput(attrs={"class":"form-control"})
        }


# ListingPictureFormset = inlineformset_factory(
#     Listing,
#     ListingPicture,
#     fields = ('name', 'picture', 'is_feature'),
#     extra = 6
# )

class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset = Agent.objects.none())

#     def __init__(self, *args, **kwargs):
