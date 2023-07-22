from django.contrib import admin
from .models import PrivacyPolicy, Service, TermsAndCondition


class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    # list_editable = ('question', 'answer', 'is_active')
    list_filter = ('is_active', 'created_at', 'updated_at')
    read_only_fields = ('created_at', 'updated_at')
    search_fields = ('title', 'policy')

admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'is_active', 'created_at', 'updated_at')
    # list_editable = ('question', 'answer', 'is_active')
    list_filter = ('is_active', 'created_at', 'updated_at')
    read_only_fields = ('created_at', 'updated_at')
    search_fields = ('title', 'description')

admin.site.register(Service, ServiceAdmin)


class TermsAndConditionAdmin(admin.ModelAdmin):
    list_display = ('term', 'is_active', 'created_at', 'updated_at')
    # list_editable = ('question', 'answer', 'is_active')
    list_filter = ('is_active', 'created_at', 'updated_at')
    read_only_fields = ('created_at', 'updated_at')
    search_fields = ('term',)

admin.site.register(TermsAndCondition, TermsAndConditionAdmin)