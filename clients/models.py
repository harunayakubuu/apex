from django.db import models
from django.conf import settings
from listings.choices import STATE_CHOICES

from phonenumber_field.modelfields import PhoneNumberField

from listings.validators import validate_picture_size
from .validators import validate_file_type

User = settings.AUTH_USER_MODEL

class Client(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    state = models.CharField(max_length=32, choices=STATE_CHOICES)
    home_address = models.CharField(max_length = 250)
    business_address = models.CharField(max_length = 250)
    GENDER_CHOICES = (
        ('f', 'Female'),
        ('m', 'Male')
    )
    gender = models.CharField(max_length = 6, choices = GENDER_CHOICES)
    # Dimension: Width - 150px, Height - 150px
    profile_picture = models.ImageField(upload_to = 'pictures/clients/profile-pictures/', null = True, blank = True, help_text="Displayed on your account's profile")
    is_verified  = models.BooleanField(default = False)
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    first_name = models.CharField(max_length = 100)
    middle_name = models.CharField(max_length = 100, null = True, blank = True)
    last_name = models.CharField(max_length = 100)
    phone_number = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True, blank = True, null = True)
    state = models.CharField(max_length=32, choices=STATE_CHOICES)
    local_government_area = models.CharField(max_length = 120)
    home_address = models.CharField(max_length = 250)
    business_address = models.CharField(max_length = 250)
    GENDER_CHOICES = (
        ('f', 'Female'),
        ('m', 'Male')
    )
    gender = models.CharField(max_length = 6, choices = GENDER_CHOICES)
    
    identification = models.FileField(validators = [validate_file_type], help_text = 'PDF format of any of National ID Card, International Passport or Drivers Licence')
    # Dimension: Width - 150px, Height - 150px
    picture = models.ImageField(upload_to = 'pictures/customer/', validators=[validate_picture_size], null = True, blank = True, help_text="Displayed on your account's profile")
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'Customer: {self.last_name} {self.first_name} {self.middle_name}'