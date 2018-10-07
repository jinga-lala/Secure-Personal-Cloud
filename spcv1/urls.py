from django.conf.urls import url
from . import views

app_name = 'spcv1'

urlpatterns = [
	url(r'^$', views.register, name='register'),
]
