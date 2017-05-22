from django.conf.urls import url

from customauth import views

app_name = 'customauth'

urlpatterns = [
    url(r'^register/$', views.register_user, name='register'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
]
