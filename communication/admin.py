from django.contrib import admin
from django.contrib.auth.models import User
from .models import Messages, UserStatus, Groups

# Register your models here.
admin.site.register(Messages)

class messagesTable(admin.ModelAdmin):
    list_display = ('id', 'text', 'owner', 'timestamp', 'recipient', 'isGroup', 'groupId', 'approval_status')
    # list_display = ('id', 'owner')

class userStatusTable(admin.ModelAdmin):
    list_display = ('id', 'owner', 'reader', 'onGroup', 'groupId', 'typing_status', 'timestamp')

class groupsTable(admin.ModelAdmin):
    list_display = ('id', 'groupId', "groupName", "owner", "description", "protectedStatus", "members", "totalMembers", "groupStatus", "timestamp")

admin.site.unregister(Messages)
admin.site.register(Messages, messagesTable)
admin.site.register(UserStatus, userStatusTable)
admin.site.register(Groups, groupsTable)
