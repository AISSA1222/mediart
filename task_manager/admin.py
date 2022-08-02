from django.contrib import admin
from .models import User, Task, Project, Client, Message, Notification

from import_export.admin import ExportActionMixin
from import_export import resources


# Register your models here.
class ClientAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('client_name', 'company_name', 'email_address', 'phone_number', 'geo_address')


admin.site.register(User)
admin.site.register(Task)
admin.site.register(Project)
admin.site.register(Client,ClientAdmin)
admin.site.register(Message)
admin.site.register(Notification)
