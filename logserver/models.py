from django.db import models


class KitBox(models.Model):
    modem_id = models.IntegerField()
    last_ping = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"KitBox #{self.modem_id}. Last ping {self.last_ping}"
