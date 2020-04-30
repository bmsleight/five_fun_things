"""five_fun_things URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), 
    path('accounts/', TemplateView.as_view(template_name='accounts.html')),
    path('things/', include('funthings.urls')), 
    path('manifest.json', TemplateView.as_view(template_name='manifest.json')), # Really poor but needs to be root
    path('service-worker.js', TemplateView.as_view(template_name='service-worker.js', content_type="application/x-javascript")),
    path('script.js', TemplateView.as_view(template_name='script.js', content_type="application/x-javascript")),
    path('', TemplateView.as_view(template_name='index.html')), 
    #worker_script
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
