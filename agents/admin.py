from django.contrib import admin
from .models import Agent

# Import-Export
from import_export import resources
from import_export.fields import Field
from import_export.admin import ExportActionMixin


class AgentResource(resources.ModelResource):
    user = Field()
    class Meta:
        model = Agent
        fields = ('user', 'additional_phone_number', 'is_active', 'hire_date', 'updated_date')
    
    def dehydrate_user(self, obj):
        return obj.user.username

class AgentAdmin(ExportActionMixin, admin.ModelAdmin):
    resoure_class = AgentResource

    raw_id_fields = ['user']
    list_display = ['user', 'additional_phone_number', 'is_active', 'hire_date', 'updated_date']
    list_filter = ['hire_date', 'updated_date']
    readonly_fields = ('hire_date', 'updated_date')
admin.site.register(Agent, AgentAdmin)