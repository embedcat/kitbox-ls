import logging
import os

from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config import settings
from logserver import services
from django import views

from logserver.models import KitBox

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
        pings_all = KitBox.objects.count()
        pings_week = [KitBox.objects.filter(last_ping__date=datetime.now() - timedelta(days=i)).count() for i in range(7)]

        return render(
                request=request,
                template_name='logserver/ping_stat.html',
                context={
                    'pings_all': pings_all,
                    'pings_week': pings_week,
                }
            )


class APILog(APIView):
    @staticmethod
    def get(request, id, start):
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def post(request, id, start):
        # start: 0 - new, 1 - continue, 2 - finalize
        logger.info(f"[URL]: {request.get_full_path()} | POST request data: {request.data}")
        if 'file' not in request.FILES and start != 2:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if start == 2:
            services.finalize_log(id=id)
            return Response(status=status.HTTP_200_OK)

        if start == 0:
            kitbox, created = KitBox.objects.get_or_create(modem_id=id, defaults={'modem_id': id})
            kitbox.last_log = timezone.now()
            kitbox.save()
            services.create_logs_dir(id=id)
            services.create_log_file(id=id)
        result = services.append_log(id=id, file_obj=request.FILES['file'])

        return Response(status=status.HTTP_200_OK) if result else Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class APIPing(APIView):
    @staticmethod
    def get(request, id):
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def post(request, id):
        kitbox, created = KitBox.objects.get_or_create(modem_id=id, defaults={'modem_id': id})
        kitbox.save()
        return Response(status=status.HTTP_200_OK)


class APITestSmall(APIView):
    @staticmethod
    def get(request):
        return Response({i: '1234567890_'*10 for i in range(5)}, status=status.HTTP_200_OK)


class APITestBig(APIView):
    @staticmethod
    def get(request):
        return Response({i: '1234567890_'*10 for i in range(15)}, status=status.HTTP_200_OK)


class APIServer(APIView):
    @staticmethod
    def get(request):
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        logger.info(f"[URL]: {request.get_full_path()} | request data: {request.data}")
        return Response(status=status.HTTP_200_OK)


class APIPosTest(APIView):
    @staticmethod
    def get(request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @staticmethod
    def post(request):
        services.pos_append_log(request.data)

        return Response(status=status.HTTP_200_OK)


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
