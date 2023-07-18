from django.db import models
from accounts.models import Profile
from django.utils.text import slugify
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

from django.conf import settings

from listings.validators import validate_picture_size
from . validators import validate_file_type

from listings.choices import STATE_CHOICES

User = settings.AUTH_USER_MODEL


class Organisor(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    state = models.CharField(max_length=32, choices=STATE_CHOICES)
    local_government_area = models.CharField(max_length = 64)
    home_address = models.CharField(max_length = 250)
    business_address = models.CharField(max_length = 250)
    GENDER_CHOICES = (
        ('f', 'Female'),
        ('m', 'Male')
    )
    gender = models.CharField(max_length = 6, choices = GENDER_CHOICES)
    # Dimension: Width - 150px, Height - 150px
    profile_picture = models.ImageField(upload_to = 'pictures/organisors/profile-pictures/', null = True, blank = True, help_text="Displayed on your account's profile")
    ID_TYPE_CHOICES = (
        ('DL', 'Drivers License'),
        ('IP', 'International Passport'),
        ('NID', 'National ID Card'),
        ('VC', 'Voter Card'),
    )
    identification_type = models.CharField(max_length = 22, choices = ID_TYPE_CHOICES)
    identification = models.FileField(validators = [validate_file_type], help_text = "Scan PDF copy")
    is_verified  = models.BooleanField(default = False)
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.user.username


class Agency(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length = 255, unique = True)
    
    rc_number = models.CharField(max_length = 50, blank = True, null = True)
    address = models.CharField(max_length = 255)
    city = models.CharField(max_length = 100)
    state = models.CharField(max_length = 50, choices = STATE_CHOICES)
    
    logo = models.ImageField(upload_to = 'pictures/agencies/logo/', validators = [validate_picture_size], help_text = "Width - 312px, Height - 286px")
    
    phone_number = PhoneNumberField()
    whatsapp_number = PhoneNumberField(blank = True, null = True)
    office_phone = PhoneNumberField(blank = True, null = True)
    email = models.EmailField(max_length = 50, unique = True, null = True, blank = True)

    about = models.TextField(blank = True, null=True)

    location_lat = models.FloatField(blank = True, null = True)
    location_lon = models.FloatField(blank = True, null = True)

    slug = models.SlugField(max_length = 255, blank = True, null = True)
    is_verified = models.BooleanField('Verified', default = False)

    STATUS_CHOICES = (
        ('APPROVED', 'Approved'),
        ('PENDING', 'Pending Approval'),
        ('DISAPPROVED', 'Disapproved'),
    )
    status = models.CharField(max_length = 20, choices = STATUS_CHOICES, default = 'PENDING')

    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('agencies:public-agency-details', args=[ str(self.slug)])

    class Meta:
        verbose_name_plural = 'Agencies'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Agency, self).save(*args, **kwargs)