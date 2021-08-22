from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from logserver.serializers import MsgSerializer


class TestView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        print("Post request:", request.data)
        s = MsgSerializer(data=request.data)
        print(s.is_valid())
        print(s.data)
        return Response(status=status.HTTP_200_OK)
