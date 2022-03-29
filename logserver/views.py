import logging

from django.shortcuts import render, redirect
from datetime import datetime, timedelta

from config import settings
from logserver import services
from django import views

from logserver.forms import MQTTDeviceAddForm, MQTTCmdForm
from logserver.models import KitBox, MQTTDevice, Event

from mqtt import mqtt_logic

logger = logging.getLogger(settings.LOGGER)


class MainView(views.View):
    @staticmethod
    def get(request):
        return redirect('logs')


class LogsView(views.View):
    @staticmethod
    def get(request):
        dir_list = services.get_id_dirs()
        items = []
        for d in dir_list:
            size = len(services.get_list_of_logs(id=int(d)))
            try:
                kitbox = KitBox.objects.get(modem_id=int(d))
                last_log = kitbox.last_log
                last_ping = kitbox.last_ping
            except KitBox.DoesNotExist:
                last_log = ""
                last_ping = ""
            items.append(dict(id=d, size=size, last_log=last_log, last_ping=last_ping))
        return render(
            request=request,
            template_name='logserver/logs.html',
            context={
                'items': items,
            }
        )


class LogsIdView(views.View):
    @staticmethod
    def get(request, id):
        dir_list = services.get_list_of_logs(id=id)
        return render(
            request=request,
            template_name='logserver/logs_id.html',
            context={
                'id': id,
                'items': dir_list,
            }
        )


class LogsDownload(views.View):
    @staticmethod
    def get(request, id, file):
        return services.download_file_response(id, file)


class LogParseAndDownload(views.View):
    @staticmethod
    def get(request, id, file):
        parsed = services.parse_log(id, file)
        if parsed is not None:
            return services.download_file_response(id, parsed)
        return redirect("logs_id", id)


class PingView(views.View):
    @staticmethod
    def get(request):
        kits = KitBox.objects.all()
        return render(
            request=request,
            template_name='logserver/ping.html',
            context={
                'items': kits,
            }
        )


class PingStatView(views.View):
    @staticmethod
    def get(request):
        # mqtt.mqtt_publish_cmd(123, cmd=mqtt.MqttCmd.publish_on)
        pings_all = KitBox.objects.count()
        pings_week = [KitBox.objects.filter(last_ping__date=datetime.now() - timedelta(days=i)).count() for i in
                      range(7)]

        return render(
            request=request,
            template_name='logserver/ping_stat.html',
            context={
                'pings_all': pings_all,
                'pings_week': pings_week,
            }
        )


class PosTestView(views.View):
    @staticmethod
    def get(request):
        return render(
            request=request,
            template_name='logserver/pos_test.html',
            context={
                'items': services.pos_get_log_lines(),
            }
        )


class MQTTView(views.View):
    @staticmethod
    def get(request):
        items = MQTTDevice.objects.all()
        return render(
            request=request,
            template_name='logserver/mqtt.html',
            context={
                'form': MQTTDeviceAddForm(),
                'items': items,
            }
        )

    @staticmethod
    def post(request):
        form = MQTTDeviceAddForm(request.POST)
        if form.is_valid():
            modem_id = form.cleaned_data['modem_id']
            MQTTDevice.objects.create(modem_id=modem_id)
            return redirect('mqtt')
        items = MQTTDevice.objects.all()
        return render(
            request=request,
            template_name='logserver/mqtt.html',
            context={
                'form': form,
                'items': items,
            }
        )


class MQTTDeviceView(views.View):
    @staticmethod
    def get(request, modem_id):
        device = MQTTDevice.objects.get(modem_id=modem_id)
        events = Event.objects.filter(device=device).order_by("-received_at")
        return render(
            request=request,
            template_name='logserver/mqtt_device.html',
            context={
                'form': MQTTCmdForm(),
                'device': device,
                'events': events,
            }
        )

    @staticmethod
    def post(request, modem_id):
        device = MQTTDevice.objects.get(modem_id=modem_id)
        events = Event.objects.filter(device=device).order_by("-received_at")
        form = MQTTCmdForm(request.POST)
        if form.is_valid():
            cmd = form.cleaned_data['cmd']
            publish_filter = form.cleaned_data['publish_filter']
            logger_filter = form.cleaned_data['logger_filter']
            payload = ""
            if cmd == str(mqtt_logic.MqttCmd.publish_filter.value):
                payload = ";".join(publish_filter) + ";" if len(publish_filter) else ""
            if cmd == str(mqtt_logic.MqttCmd.logger_start.value):
                payload = ";".join(logger_filter) + ";" if len(logger_filter) else ""
            mqtt_logic.mqtt_publish_cmd(modem_id=modem_id,
                                        cmd=int(cmd),
                                        payload=payload)
            return redirect('mqtt_device', modem_id)
        return render(
            request=request,
            template_name='logserver/mqtt_device.html',
            context={
                'form': form,
                'device': device,
                'events': events,
            }
        )
