from django.contrib import admin

from logserver.models import KitBox, MQTTDevice

admin.site.register(KitBox)
admin.site.register(MQTTDevice)
