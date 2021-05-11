from django.db import models
from django.contrib.humanize.templatetags import humanize


# Create your models here.
class Messages(models.Model):
    text = models.TextField(blank=False, unique=False)
    owner = models.CharField(max_length=50, unique=False)
    timestamp = models.DateTimeField(auto_now_add=True, unique=False, editable=True)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return ("MESSAGE : {} | sent by {} | at {} | is typing : {}".format(self.text, self.owner, self.timestamp, self.status))

    def get_time_humanised(self):
        return humanize.naturaltime(self.timestamp)

    def get_items_as_dict(self):
        return dict({"id": self.id, "owner": self.owner, "text": self.text, "timestamp": self.get_time_humanised(), "typing_status": self.status})


