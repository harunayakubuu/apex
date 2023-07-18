from django.contrib import admin
from .models import Report
# Register your models here.


class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'created', 'updated')

admin.site.register(Report, ReportAdmin)