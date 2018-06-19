from django.conf.urls import url
from django.urls import path, re_path
import re

from polls import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^upload/', views.uploadfun, name='uploadfun'),
]