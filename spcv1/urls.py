from django.conf.urls import url
from . import views

app_name = 'spcv1'

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^home$', views.home, name='home'),
	url(r'^signup$', views.signup, name='signup'),
    url(r'^files$', views.FileTree, name='files'),
    url(r'^token$',views.getToken,name='token')
]
