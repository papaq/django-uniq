from django.conf.urls import url
from . import views

app_name = 'channels'

urlpatterns = [
    url(r'^$', views.channels_list, name='channels-list'),
    url(r'^index$', views.channels_list, name='index'),
]
