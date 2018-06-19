from django.conf.urls import url
from django.urls import path, re_path
import re

from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    #re_path(r'^more/$', views.more, name='more'),
]