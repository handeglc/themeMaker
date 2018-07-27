from django.urls import path, re_path
#from django.conf import settings
#from django.conf.urls.static import static

from polls import views
from polls.views import *


urlpatterns = [
    re_path(r'^logout/', views.logout_view, name='logout_view'),
    re_path(r'^index/', LoginView.as_view()),
    re_path(r'^signup/', views.SignUpView.as_view()),
    re_path(r'^delete_cg/', views.delete_cg_view, name='delete_cg_view'),
    re_path(r'^recommend/', RecommendationView.as_view(), name='user_recommendation_list'),
    re_path(r'^save/', SaveView.as_view()),
    re_path(r'^show_cg/', views.show_cg_view, name='show_cg'),
    re_path(r'^$', LoginView.as_view()),
    re_path(r'^upload/recommend/', RecommendationView.as_view(), name='user_recommendation_list'),
    re_path(r'^upload/save/', SaveView.as_view()),
    re_path(r'^upload/', UploadView.as_view()),
    re_path(r'api/login/', ReactApiView.as_view())
]#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)