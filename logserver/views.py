import logging
import os

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config import settings
from logserver.serializers import MsgSerializer
from logserver import services
from django import views

logger = logging.getLogger(settings.LOGGER)


class BrowserView(views.View):
    @staticmethod
    def get(request):
        dir_list = services.get_id_dirs()
        return render(
                request=request,
                template_name='logserver/browser.html',
                context={
                    'items': dir_list,
                }
            )


class BrowserIdView(views.View):
    @staticmethod
    def get(request, id):
        dir_list = services.get_id_dirs(id)
        return render(
                request=request,
                template_name='logserver/browser_id.html',
                context={
                    'id': id,
                    'items': dir_list,
                }
            )


class BrowserDownloadFile(views.View):
    @staticmethod
    def get(request, id, file):
        return services.download_file_response(id, file)


class TestView(APIView):
    @staticmethod
    def get(request):
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        print("Post request:", request.data)
        s = MsgSerializer(data=request.data)
        print(s.is_valid())
        print(s.data)
        logger.info(f"[POST] request data: {request.data}")
        if s.is_valid():
            if s.data['start']:
                services.create_logs_dir(id=s.data['id'])
            if s.data['data']:
                services.append_log(id=s.data['id'], data=s.data['data'], start_new_file=s.data['start'])
        return Response(status=status.HTTP_200_OK)


class APILog(APIView):
    @staticmethod
    def get(request, id, start):
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def post(request, id, start):
        s = MsgSerializer(data=request.data)
        logger.info(f"[POST] request data id={id}, start={start}: {request.data}")
        f = request.FILES['file']

        with open('name.txt', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        if s.is_valid():
            if start == 1:
                services.create_logs_dir(id=id)
            if s.data['data']:
                services.append_log(id=id, data=s.data['data'], start_new_file=(start == 1))
        return Response(status=status.HTTP_200_OK)
