from django.conf.urls import url
from django.urls import path, re_path
import re

from polls import views
from polls.views import *

urlpatterns = [
    re_path(r'^logout/', views.logout_view, name='logout_view'),
    re_path(r'^index/', LoginView.as_view()),
    re_path(r'^$', LoginView.as_view()),
    re_path(r'^upload/save/', SaveView.as_view()),
    re_path(r'^upload/', UploadView.as_view()),
]