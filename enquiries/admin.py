from django.contrib import admin
from .models import Enquiry


class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'user_phone', 'user_email', 'created_at')
    list_per_page = 25
    search_fields = ('user_email', 'user_name')
    list_display_links = ('user_email', 'user_phone')
    readonly_fields = ('created_at',)
    list_filter = ('created_at',)

admin.site.register(Enquiry, EnquiryAdmin)