from django.conf.urls import url, include
from . import views

app_name = 'channels'

channels_urlpatterns = [

]

urlpatterns = [
    url(r'^stream/$', views.stream, name='stream'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),

    url(r'^channels/', include(channels_urlpatterns)),
]
