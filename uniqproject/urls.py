"""uniqproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from channels import urls as channels_urls
from customauth import urls as customauth_urls
from post import urls as post_urls
from dialogue import urls as dialogue_urls
from . import views as base_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', base_views.redirect_to_stream),
    url(r'^channels/', include(channels_urls)),

    url(r'^post/', include(post_urls)),
    url(r'^account/', include(customauth_urls)),
    url(r'^dialogue/', include(dialogue_urls)),

    # url(r'^.+$', base_views.redirect_to_stream)
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
