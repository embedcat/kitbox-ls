from django.urls import path

from logserver.views import TestView, BrowserView, BrowserIdView, BrowserDownloadFile

urlpatterns = [
    path('', BrowserView.as_view(), name='browser'),
    path('b/<int:id>/', BrowserIdView.as_view(), name='browser_id'),
    path('b/<int:id>/<str:file>', BrowserDownloadFile.as_view(), name='browser_download_file'),

    path('api/v0/', TestView.as_view(), name='log'),
]