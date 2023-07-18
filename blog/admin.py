from django.contrib import admin
from .models import Category, Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('is_active', 'created_at', 'updated_at')

admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('is_active', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)