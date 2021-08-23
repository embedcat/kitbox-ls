import os

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from logserver.serializers import MsgSerializer
from logserver import services
from django import views


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
        if s.is_valid():
            if s.data['start']:
                services.create_logs_dir(id=s.data['id'])
            if s.data['data']:
                services.append_log(id=s.data['id'], data=s.data['data'], start_new_file=s.data['start'])
        return Response(status=status.HTTP_200_OK)
