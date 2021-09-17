from django.urls import path

from logserver.views import LogsView, LogsIdView, LogsDownload, APILog, APIPing, PingView, MainView, APIServer, \
    LogParseAndDownload

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('logs/', LogsView.as_view(), name='logs'),
    path('logs/<int:id>/', LogsIdView.as_view(), name='logs_id'),
    path('logs/<int:id>/<str:file>', LogsDownload.as_view(), name='logs_download'),
    path('logs/<int:id>/<str:file>/parse', LogParseAndDownload.as_view(), name='logs_parse'),
    path('ping/', PingView.as_view(), name='ping'),

    path('api/v0/<int:id>/<int:start>/', APILog.as_view(), name='api_log'),
    path('api/v0/<int:id>/ping/', APIPing.as_view(), name='api_ping'),
    path('api/v0/server/', APIServer.as_view(), name='api_server'),

]
