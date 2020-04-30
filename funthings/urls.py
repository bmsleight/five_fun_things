from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    path('<int:year>/<int:month>/<int:day>/',
         views.five_fun_form, name='five_fun_form'),
    path('journal/', views.date_view),
    path('cloud/', login_required(TemplateView.as_view(template_name='cloud.html'))),
    path('cloud/cloud.png', views.cloud_view),
    path('', views.ThingList.as_view(), name='list'),
    ]
      
