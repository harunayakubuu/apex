from django.db import models
from django.conf import settings


# Create your models here.
User = settings.AUTH_USER_MODEL

class Report(models.Model):
    name = models.CharField(max_length = 128)
    image = models.ImageField(upload_to = 'pictures/reports', blank = True)
    remark = models.TextField()
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return f"Report for: {self.name}, by: {self.author}"