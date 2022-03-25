from django.db import models
from django.utils import timezone
from mqtt.mqtt_logic import get_mqtt_events_list, MqttEvent


class KitBox(models.Model):
    modem_id = models.IntegerField()
    last_ping = models.DateTimeField(auto_now=True)
    last_log = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"KitBox #{self.modem_id}. Last ping {self.last_ping}"


class MQTTDevice(models.Model):
    modem_id = models.IntegerField()
    add_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"MQTT device {self.modem_id}"


def get_event_choices() -> list:
    return get_mqtt_events_list()


class Event(models.Model):
    device = models.ForeignKey(MQTTDevice, related_name="device", on_delete=models.CASCADE)
    received_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=5, choices=get_event_choices(), default=0)
    payload = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        e = MqttEvent(int(str(self.type)))
        return f"Event to \"{self.device}\", type={e.name}({e.value}), msg=\"{self.payload}\" at {self.received_at}"
