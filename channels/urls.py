from django.conf.urls import url, include
from . import views

app_name = 'channels'

channels_urlpatterns = [
    url(r'^$', views.channels_list, name='channels-list'),
    url(r'^index$', views.channels_list, name='index'),
]

urlpatterns = [
    url(r'^$', views.initial, name='initial'),
    url(r'^channels/', include(channels_urlpatterns)),
]
