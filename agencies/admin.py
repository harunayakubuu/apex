from django.contrib import admin
from .models import Agency, Organisor


class AgencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'city', 'state', 'status']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Agency, AgencyAdmin)

class OrganisorAdmin(admin.ModelAdmin):
    list_display = ['user', ]
    # prepopulated_fields = {'slug': ('name',)}
admin.site.register(Organisor, OrganisorAdmin)