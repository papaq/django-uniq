from django.conf.urls import url, include
from . import views

app_name = 'channels'

channels_urlpatterns = [

]

urlpatterns = [
    url(r'^stream/$', views.stream, name='stream'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^go-to-dialogue/(?P<user_pk>\d+)$', views.GoToDialogueView.as_view(), name='go_to_dialogue'),

    # url(r'^channels/', include(channels_urlpatterns)),
]
