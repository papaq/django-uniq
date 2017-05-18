from django.conf.urls import url
from . import views

app_name = 'registration'

urlpatterns = [
    url(r'^$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
]