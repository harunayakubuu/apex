from django.db import models
from ckeditor.fields import RichTextField


# class AboutUs(models.Model):
#     # title = models.CharField(max_length = 255)
#     about = RichTextField()
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)


class PrivacyPolicy(models.Model):
    title = models.CharField(max_length = 255)
    policy = RichTextField()
    is_active = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Privacy Policy"


class TermsAndCondition(models.Model):
    term = models.CharField(max_length = 255)
    condition = RichTextField()
    is_active = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.term


class Service(models.Model):
    title = models.CharField(max_length = 255, unique = True)
    description = models.TextField()
    is_active = models.BooleanField("Active", default = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title