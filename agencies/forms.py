from django import forms
from .models import Agency, Organisor
from django.contrib.auth import get_user_model

User = get_user_model()

# Registering User Organisor from the admin dashboard
class AdminOrganisorUserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')

        help_texts = {
            'username': None,
        }


# Updating User Organisor from the admin dashboard
class AdminOrganisorUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_active', )


# Creating the main organisor table
class OrganisorCreateForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('m', "Male"),
        ('f', "Female"),
    )
    gender = forms.ChoiceField(choices= GENDER_CHOICES, widget = forms.RadioSelect())
    class Meta:
        model = Organisor
        fields = ('state', 'home_address', 'business_address', 'gender', 'profile_picture', 'identification_type', 'identification')
        
        widgets = {
            'state': forms.Select(attrs = {'class': 'form-select'}),
            'identification_type': forms.Select(attrs = {'class': 'form-select'}),
        }


# Updating the main organisor table
class OrganisorUpdateForm(forms.ModelForm):    
    class Meta:
        model = Organisor
        fields = ('state', 'home_address', 'business_address', 'profile_picture', 'identification_type', 'identification')

        widgets = {
            'state': forms.Select(attrs = {'class': 'form-select'}),
            'identification_type': forms.Select(attrs = {'class': 'form-select'}),
        }


class AgencyCreateForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = [
            'name', 'rc_number','logo',
            'address', 'city', 'state', 'phone_number', 'office_phone',
            'whatsapp_number', 'email', 'about', 'rc_number'
        ]

        labels = {
            'name': 'Agency Name',
            'address': 'Agency Address',
            'city': 'City',
            'phone_number': 'Agency Phone',
            'whatsapp_number': 'WhatsApp Number',
            'email': 'Agency Email',
            'rc_number': "Registration Number (RC/BN)"
        }

        widgets = {
            'name': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Agency Name'}),
            'rc_number': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'RC Number'}),
            'address': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Full address. E.g No. C250, ABC Road'}),
            'city': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'City'}),
            'email': forms.EmailInput(attrs = {'class': 'form-control', 'placeholder': 'Agency Contact Email'}),
            'rc_number': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'RC/BN'}),

        }
    
    def clean(self):
        data = self.cleaned_data
        name = data.get('name')
        qs = Agency.objects.filter(name__iexact=name)
        if qs.exists():
            self.add_error('name', f"The name, '{name}' has already exist.")
        return data


class AgencyUpdateForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = ['name', 'address', 'phone_number', 'whatsapp_number', 'office_phone', 'email', 'city', 'state', 'logo', 'about']

        labels = {
            'name': 'Agency Name',
            'address': 'Agency Address',
            'phone_number': 'Agency Phone',
            'email': 'Agency Email'
        }

        widgets = {
            'name': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Agency Name', 'readonly':'readonly'}),
            'address': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Full address. E.g No. C250, ABC Road'}),
            'email': forms.EmailInput(attrs = {'class': 'form-control', 'placeholder': 'Agency Contact Email'}),
        }


class AdminAgencyUpdateForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = ['status', 'is_verified']

        # labels = {
        #     'name': 'Agency Name',
        #     'address': 'Agency Address',
        #     'phone_number': 'Agency Phone',
        #     'email': 'Agency Email'
        # }

        widgets = {
            'status': forms.Select(attrs = {'class': 'form-select'}),
            # 'name': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Agency Name'}),
            # 'address': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Full address. E.g No. C250, ABC Road'}),
            # 'email': forms.EmailInput(attrs = {'class': 'form-control', 'placeholder': 'Agency Contact Email'}),
        }