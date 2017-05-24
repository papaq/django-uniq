from django.conf.urls import url, include

from customauth import views

app_name = 'customauth'

subscription_url_patterns = [
    url(r'^university/$', views.subscribe_university, name='subscribe_university'),
    url(r'^faculty/$', views.subscribe_faculty, name='subscribe_faculty'),
    url(r'^group/$', views.subscribe_group, name='subscribe_group'),
    url(r'^(?P<channel>\w+)/$', views.subscription, name='subscription'),
]

unsubscription_url_patterns = [
    url(r'^university/user(?P<pk>\d+)/$', views.unsubscribe_university, name='unsubscribe_university'),
    url(r'^faculty/user(?P<pk>\d+)/$', views.unsubscribe_faculty, name='unsubscribe_faculty'),
    url(r'^group/user(?P<pk>\d+)/$', views.unsubscribe_group, name='unsubscribe_group'),
    url(r'^(?P<channel>\w+)/$', views.unsubscription, name='unsubscription'),
]

profile_url_patterns = [
    url(r'^$', views.profile, name='profile'),
    url(r'^user(?P<pk>\d+)/avatar/delete/$', views.avatar_delete, name='avatar_delete'),
    url(r'^subscribe/', include(subscription_url_patterns)),
    url(r'^unsubscribe/', include(unsubscription_url_patterns))
]

urlpatterns = [
    url(r'^register/$', views.register_user, name='register'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^profile/', include(profile_url_patterns)),
]
