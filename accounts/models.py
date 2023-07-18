from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse

from phonenumber_field.modelfields import PhoneNumberField

from listings.validators import validate_picture_size


class User(AbstractUser):
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)
    is_organisor = models.BooleanField('Agency', default = False)
    is_agent = models.BooleanField("Agent", default = False)
    is_client = models.BooleanField("Client", default = False)

    def get_full_name(self):
        #Return the first_name plus the last_name, with a space in between.
        if self.middle_name:
            full_name = '%s %s %s' %(self.first_name, self.middle_name, self.last_name)
        else:
            full_name = '%s %s' %(self.first_name, self.last_name)

        return full_name.strip()

    def get_short_name(self):
        #Return the short name for the user.
        return self.first_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'{self.user.username} - {self.user.email}'


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)
        
post_save.connect(post_user_created_signal, sender=User)


class Team(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    DESIGNATION_CHOICES = (
        ('ceo', 'MD/CEO'),
        ('business_consultant', 'Business Consultant'),
        ('it_consultant', 'IT Consultant'),
        ('legal_consultant', 'Legal Consultant'),
    )
    designation = models.CharField(max_length = 20, choices = DESIGNATION_CHOICES)
    words = models.CharField(max_length = 100)
    picture = models.ImageField(upload_to = 'pictures/team/', validators = [validate_picture_size], help_text = 'Width: 430px, Height: 450px')
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.user.email}'