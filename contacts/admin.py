from django.contrib import admin
from . models import Contact, BranchOffice, EmergencyContact

# Django Import-Export
from import_export import resources
from import_export.fields import Field
from import_export.admin import ExportActionMixin


class ContactResource(resources.ModelResource):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone', 'message', 'status', 'created_at')

class ContactAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = ContactResource
    list_display = ('name', 'email', 'phone', 'message', 'status', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('message', 'created_at', 'updated_at')
    list_filter = ('created_at', 'status')
admin.site.register(Contact, ContactAdmin)


class BranchOfficeAdmin(admin.ModelAdmin):
    list_display = ('state', 'address', 'phone', 'email', 'is_active')
    list_filter = ('is_active', 'created_at', 'updated_at')
    read_only_fields = ('created_at', 'updated_at')
admin.site.register(BranchOffice, BranchOfficeAdmin)


class EmergencyContactResource(resources.ModelResource):
    user = Field()
    class Meta:
        model = EmergencyContact
        fields = ('user', 'full_name', 'email', 'phone', 'relationship', 'address', 'state', 'created_at')

    # Allows to return the actual value of a foreignkey instead of intiger values.
    def dehydrate_user(self, obj):
        return obj.user.username

class EmergencyContactAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = EmergencyContactResource
    list_filter = ('created_at',)
    list_display = ('user', 'full_name', 'email', 'phone', 'relationship', 'address', 'state', 'created_at')
    search_fields = ('full_name', 'phone', 'address')

admin.site.register(EmergencyContact, EmergencyContactAdmin)
