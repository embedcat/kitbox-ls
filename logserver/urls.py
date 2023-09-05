from django.urls import path

from logserver.views import MainView

from logserver.APIviews import APICmd

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('api/cmd', APICmd.as_view(), name='api_cmd'),
]
