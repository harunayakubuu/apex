from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# from twilio.rest import Client

class Enquiry(models.Model):
    listing_id = models.CharField(max_length = 255)
    listing = models.CharField(max_length = 255)
    locaction = models.CharField(max_length = 255)
    user_id = models.PositiveIntegerField(blank=True)
    user_slug = models.CharField(max_length = 255, blank=True)
    user_name = models.CharField(max_length = 255)
    user_email = models.CharField(max_length = 255)
    user_phone = PhoneNumberField()
    message = models.TextField()
    is_contacted = models.BooleanField("Contacted", default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Enquiries'
        ordering = ('-created_at',)

    def __str__(self):
        return self.user_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)