from django import template
from mqtt.mqtt_logic import get_mqtt_event_name

register = template.Library()


@register.filter
def event_name(event):
    # e = int(event.type)
    return get_mqtt_event_name(int(event))
