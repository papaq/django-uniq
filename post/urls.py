from django.conf.urls import url
from . import views

app_name = 'post'

urlpatterns = [
    url(r'^new/$', views.new_post, name='new-post'),
]
