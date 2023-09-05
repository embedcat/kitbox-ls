import logging

from django.shortcuts import render, redirect
from datetime import datetime, timedelta

from config import settings
from logserver import services
from django import views

from logserver.forms import KitboxAddForm
from logserver.models import KitBox


logger = logging.getLogger(settings.LOGGER)


class MainView(views.View):
    @staticmethod
    def get(request):
        items = KitBox.objects.all()
        return render(
            request=request,
            template_name='logserver/index.html',
            context={
                'form': KitboxAddForm(),
                'items': items,
            }
        )

    @staticmethod
    def post(request):
        form = KitboxAddForm(request.POST)
        if form.is_valid():
            modem_id = form.cleaned_data['modem_id']
            KitBox.objects.create(modem_id=modem_id)
            return redirect('main')
        items = KitBox.objects.all()
        return render(
            request=request,
            template_name='logserver/index.html',
            context={
                'form': form,
                'items': items,
            }
        )

