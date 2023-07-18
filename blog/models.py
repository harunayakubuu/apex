from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from django.contrib import messages


User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length = 255)
    is_active = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


class Post(models.Model):
    author      = models.ForeignKey(User, on_delete = models.CASCADE)
    title       = models.CharField(max_length = 128, unique = True)
    slug        = models.SlugField(max_length = 150, unique = True)
    category    = models.ForeignKey(Category, on_delete = models.CASCADE)
    image       = models.ImageField(upload_to = 'pictures/blog/', help_text = "Width - 900px, Height - 540px")
    content     = models.TextField()
    is_active   = models.BooleanField("Active", default = False)
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:public-post-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)
