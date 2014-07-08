from django.conf.urls import patterns, include, url

from django.contrib import admin
from .views import *
admin.autodiscover()


urlpatterns = patterns('network.views',
    #Upload Pre-Processed file
    url(regex=r'^upload/$', view="upload_network", name="network_upload"),
    url(regex=r'^step2/$', view='step2', name='step2'),
    #Home Classification


    #url(regex=r'^delete/(?P<id>[0-9]+)/$', view="deleteFile", name="delete"),

    url(regex=r'^(.+)/$', view="network", name="network"),
    url(regex=r'^$', view="network_redirect", name="network")
    )