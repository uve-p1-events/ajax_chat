from django.db import models
from django.contrib.humanize.templatetags import humanize
import uuid

# Create your models here.
class Messages(models.Model):
    text = models.TextField(blank=False, unique=False)
    owner = models.CharField(max_length=50, unique=False)
    timestamp = models.DateTimeField(auto_now_add=True, unique=False, editable=True)
    recipient = models.CharField(max_length=50, unique=False)
    isGroup = models.BooleanField(default=False)
    groupId = models.TextField(null=True, blank=True)
    approval_status = models.BooleanField(default=False)

    def __str__(self):
        return ("MESSAGE : {} | sent by {} | at {}".format(self.text, self.owner, self.timestamp))

    def get_time_humanised(self):
        return humanize.naturaltime(self.timestamp)

    def get_items_as_dict(self):
        # return dict({"id": self.id, "owner": self.owner, "text": self.text, "timestamp": self.get_time_humanised(), "typing_status": self.status})
        return dict({"id": self.id, "owner": self.owner, "text": self.text, "timestamp": self.get_time_humanised(), "recipient": self.recipient, "isgroup": self.isGroup, "groupID": self.groupId, "normalTimestamp": self.timestamp})


class UserStatus(models.Model):
    owner = models.CharField(max_length=50, unique=False)
    reader = models.CharField(max_length=50, unique=False, null=True, blank=True)
    typing_status = models.BooleanField(default=False)
    onGroup = models.BooleanField(default=False, null=True, blank=True)
    groupId = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True, unique=False, editable=True)


    def __str__(self):
        return ("Owner : {}, reciever : {}, ongroup : {}, groupId : {}, latest_timestamp : {}".format(self.owner, self.reader, self.onGroup, self.groupId, self.timestamp))

    # def get_items_as_dict(self):
    #     return dict({"owner": self.owner, "reader": self.reader, "onGroup": self.onGroup, "groupId": self.groupId, "latestTimestamp": self.timestamp})

    def get_status(self):
        return dict({"owner": self.owner, "reader": self.reader, "typingStatus": self.typing_status})

    def get_typing_status(self):
        return self.typing_status

class Groups(models.Model):
    groupId = models.UUIDField(default=uuid.uuid4, editable=False, blank=False, unique=True)
    groupName = models.TextField(blank=False, unique=True)
    owner = models.CharField(max_length=50, unique=False)
    description = models.TextField(blank=True, unique=False)
    protectedStatus = models.BooleanField(default=False, null=False, blank=False)
    members = models.TextField(blank=True, unique=False)
    totalMembers = models.IntegerField(null=True, blank=True)
    groupStatus = models.BooleanField(default=True, null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True, unique=False, editable=False)


    def __str__(self):
        return ("groupId => {}, groupName => {}, members => {}, createdAt => {}".format(self.groupId, self.groupName, self.members, self.timestamp))