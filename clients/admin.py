from django.contrib import admin
from .models import Client, Customer

# Import-Export
from import_export import resources
from import_export.fields import Field
from import_export.admin import ExportActionMixin


class ClientResource(resources.ModelResource):
    user = Field()
    class Meta:
        model = Client
        fields = ('user', 'created_date', 'updated_date')
    
    def dehydrate_user(self, obj):
        return obj.user.username

class ClientAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = ClientResource
    
    raw_id_fields = ['user']
    list_display = ['user']
    list_filter = ['user']
admin.site.register(Client, ClientAdmin)


admin.site.register(Customer)