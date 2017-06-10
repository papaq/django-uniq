from django.conf.urls import url, include
from . import views


app_name = 'dialogue'

urlpatterns = [
    url(r'^list/$', views.dialogue_list, name='dialogue_list'),
    url(r'^(?P<dialogue_pk>\d+)/$', views.dialogue_chat, name='dialogue_chat'),

]
