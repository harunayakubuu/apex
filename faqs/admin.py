from django.contrib import admin
from .models import Faq, Testimonial


class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'is_active', 'created_at', 'updated_at')
    # list_editable = ('question', 'answer', 'is_active')
    list_filter = ('is_active', 'created_at', 'updated_at')
    read_only_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('question',)}
    search_fields = ('question', 'answer')

admin.site.register(Faq, FaqAdmin)

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'testimonial', 'is_active', 'created_at', 'updated_at')
    # list_editable = ('question', 'answer', 'is_active')
    list_filter = ('is_active', 'created_at', 'updated_at')
    read_only_fields = ('created_at', 'updated_at')
    raw_id_fields = ('user',)
    search_fields = ('user', 'testimonial')

admin.site.register(Testimonial, TestimonialAdmin)