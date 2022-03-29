from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config import settings
from logserver import services
from logserver.models import KitBox
import logging

logger = logging.getLogger(settings.LOGGER)


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
        return Response({i: '1234567890_' * 10 for i in range(5)}, status=status.HTTP_200_OK)


class APITestBig(APIView):
    @staticmethod
    def get(request):
        return Response({i: '1234567890_' * 10 for i in range(15)}, status=status.HTTP_200_OK)


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
        services.pos_append_log(str(request.data))

        return Response(status=status.HTTP_200_OK)
