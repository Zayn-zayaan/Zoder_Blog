"""Zoder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
import blog.urls
import home.urls
from . import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

from django.conf.urls import url
from django.views.static import serve

admin.site.site_header = "Zoder Admin"
admin.site.site_title = "Zoder Admin Panel"
admin.site.index_title = "Welcome to Zoder Admin Panel"

admin.autodiscover()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include(blog.urls)),
    path('', include(home.urls)),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATICFILES_DIRS}),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
