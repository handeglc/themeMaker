from django.conf.urls import url
from django.urls import path, re_path
import re

from polls import views
from polls.views import *

urlpatterns = [
    #re_path(r'^$', views.index, name='index'),
    re_path(r'^$', IndexView.as_view()),
    re_path(r'^upload/', UploadView.as_view()),
]