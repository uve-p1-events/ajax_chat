from django.contrib import admin
from django.contrib.auth.models import User
from .models import Messages

# Register your models here.
# admin.site.register(Messages)

class messageTable(admin.ModelAdmin):
    list_display = ('id', 'text', 'owner', 'timestamp')

admin.site.register(Messages, messageTable)