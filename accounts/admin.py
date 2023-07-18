from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Profile, Team

# Import-Export
from import_export import resources
from import_export.fields import Field
from import_export.admin import ExportActionMixin

User = get_user_model()


class MyAdmin(UserAdmin):
    list_display =('username', 'first_name', 'middle_name', 'last_name', 'is_active', 'is_organisor', 'is_agent', 'is_superuser', 'last_login')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'phone_number', 'first_name', 'middle_name', 'last_name', 'date_joined', 'last_login')
    ordering = ('username',)
    list_display_links = ['username',]

    list_filter = (
        ('is_agent', 'is_active')
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal Info'), {'fields': ('first_name', 'middle_name', 'last_name')}),
        (('Contact'), {'fields': ('email', 'phone_number')}),
        (('Permisions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (('User Roles'), {'fields': ('is_organisor', 'is_agent', 'is_client')}),
        (('Important Dates'), {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, MyAdmin)

class ProfileResource(resources.ModelResource):
    user = Field()
    class Meta:
        model = Profile
        fields = ('id', 'user')#, 'home_address', 'business_address', 'designation')
        export_order = ('id', 'user')#, 'designation', 'home_address', 'business_address')
    
    def dehydrate_user(self, obj):
        return obj.user.username

class ProfileAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = ProfileResource
    list_filter = ('created_date', 'updated_date')

admin.site.register(Profile, ProfileAdmin)

admin.site.register(Team)