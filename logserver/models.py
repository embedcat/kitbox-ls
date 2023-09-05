from django.db import models
from django.utils import timezone


class KitBox(models.Model):
    modem_id = models.IntegerField()
    add_at = models.DateTimeField(auto_now=True)
    log_request = models.BooleanField(default=False)

    def __str__(self):
        return f"KitBox #{self.modem_id}"
