from django.urls import path

from logserver.views import TestView

urlpatterns = [
    path('', TestView.as_view(), name='main'),
]