from django.conf.urls import url, include

from customauth import views

app_name = 'customauth'

profile_url_patterns = [
    url(r'^$', views.profile, name='profile'),
    url(r'^user(?P<pk>\d+)/avatar/delete/$', views.avatar_delete, name='avatar_delete'),
]

urlpatterns = [
    url(r'^register/$', views.register_user, name='register'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^profile/', include(profile_url_patterns)),
]
