from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from views import *

urlpatterns = [
    url(r'^$', RegisterView.as_view(), name="home"),
    url(r'^excel/$', ParticipantExcel, name="excel"),
]
