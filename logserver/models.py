from django.db import models
from django.utils import timezone


class KitBox(models.Model):
    modem_id = models.IntegerField()
    last_ping = models.DateTimeField(auto_now=True)
    last_log = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"KitBox #{self.modem_id}. Last ping {self.last_ping}"
