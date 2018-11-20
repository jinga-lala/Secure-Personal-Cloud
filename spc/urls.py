"""spc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth import views as auth_views

from spcv1 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^files/$', views.FileTree, name='files'),
    url(r'^spc/', include('spcv1.urls')),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^api/$', views.FileList.as_view()),
    url(r'^pathAPI/$',views.FileListNotData.as_view()),
    url(r'^pathAPI/(?P<user_id>[a-zA-Z0-9\-\_^/]+)/$', views.FileListNotDataUser.as_view(), name='results'),
    url(r'^api/(?P<user_id>[a-zA-Z0-9\-\_]+)/(?P<path>.+)$', views.FileListUserData.as_view(), name='file'),
    url(r'^userAPI/(?P<user_id>[a-zA-Z0-9\-\_^/]+)/$', views.UserId.as_view(), name='user'),
    url(r'^encAPI/(?P<user_id>[a-zA-Z0-9\-\_^/]+)/$', views.getEnc.as_view(), name='enc')
    ##TODO Error handling and security risks
]
urlpatterns = format_suffix_patterns(urlpatterns)
