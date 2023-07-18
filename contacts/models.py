from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
from django.contrib.auth import get_user_model

from listings.choices import STATE_CHOICES

User = get_user_model()

class Contact(models.Model):
    name  = models.CharField(max_length = 50, verbose_name='Name')
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = PhoneNumberField(verbose_name="Phone number")
    SUBJECT_CHOICES = (
        ('complaint', 'Complaint'),
        ('customer care', 'Customer Care'),
        ('Enquiries', 'Enquiries'),
        ('valuation', 'Property Valuation'),
        ('sales', 'Sales'),
    )
    subject     = models.CharField(max_length = 20, choices = SUBJECT_CHOICES)
    STATUS_CHOICES = (
        ('attended', 'Attended'),
        ('ignored', 'Ignored'),
        ('pending', 'Pending'),
    )
    message     = models.TextField()
    status      = models.CharField(max_length = 20, choices = STATUS_CHOICES, default="pending")
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

    def get_message_details(self):
        return reverse('contacts:contact-message-details', args=[self.id])


class BranchOffice(models.Model):
    state       = models.CharField(max_length=255, choices=STATE_CHOICES)
    city        = models.CharField(max_length=255)
    address     = models.CharField(max_length=255)
    phone       = PhoneNumberField()
    email       = models.EmailField()
    is_active   = models.BooleanField("Active", default=False)
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.state

    class Meta:
        verbose_name_plural = "Branch Offices"


class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    full_name = models.CharField(max_length = 255)
    phone = PhoneNumberField()
    email = models.EmailField(max_length = 255, unique = True, blank = True, null = True)
    picture = models.ImageField(upload_to = 'pictures/emergency-contacts/', help_text = "Width - 150px, Height - 150px")
    
    RELATIONSHIP_CHOICES = (
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('son', 'Son'),
        ('daughter', 'Daughter'),
        ('husband', 'Husband'),
        ('wife', 'Wife'),
        ('brother', 'Brother'),
        ('sister', 'Sister'),
        ('uncle', 'Uncle'),
        ('aunt', 'Aunt'),
        ('friend', 'Friend'),
        ('employer', 'Employer'),
        ('employee', 'Employee'),
        ('other', 'Other'),
    )
    relationship = models.CharField(max_length = 255, choices = RELATIONSHIP_CHOICES)
    address = models.CharField(max_length = 255)
    state = models.CharField(max_length = 32, choices = STATE_CHOICES)
    comment = models.TextField(blank=True, null=True)
    next_of_kin = models.BooleanField(help_text = 'Check this box if he or she is your next of kin.', default = False)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ('-user',)

    def get_edit_contact(self):
        return reverse('contacts:emergency-contact-edit', args=[self.id])