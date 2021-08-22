from django.urls import path

from logserver.views import TestView

urlpatterns = [
    path('api/v0/', TestView.as_view(), name='log'),
]