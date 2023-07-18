from django.db import models
from django.urls import reverse
from django.conf import settings

from accounts.models import Profile

from phonenumber_field.modelfields import PhoneNumberField
from listings.validators import validate_picture_size

User = settings.AUTH_USER_MODEL

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    organization = models.ForeignKey(Profile, blank = True, null = True, on_delete=models.CASCADE)
    
    additional_phone_number = PhoneNumberField(verbose_name = 'additional Phone Number', blank = True, null=True)
    # Dimension: Width - 150px, Height - 150px
    profile_picture = models.ImageField(upload_to = 'pictures/agents/profile-pictures/', validators=[validate_picture_size], null = True, blank = True, help_text="Displayed on your account's profile")
    
    # Dimension: Width - 430px, Height - 450px
    display_picture = models.ImageField(upload_to = 'pictures/agents/display-pictures/', validators=[validate_picture_size], null = True, blank = True, help_text="Displayed to the public")
    
    about = models.TextField(blank = True, null = True)

    agent_of_the_week = models.BooleanField(default=False)
    agent_of_the_month = models.BooleanField(default=False)
    agent_of_the_year = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    
    hire_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'{self.user.email} - {self.user.username}'
    
    def get_public_agent_details(self):
        return reverse('agents:public-agent-details', args=[self.user.id])

    def get_agent_details(self):
        return reverse('agents:agent-details', args=[str(self.user.username)])
