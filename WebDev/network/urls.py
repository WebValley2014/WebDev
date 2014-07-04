from django.conf.urls import patterns, include, url

from django.contrib import admin
from .views import *
admin.autodiscover()


urlpatterns = patterns('network.views',
    #Upload Pre-Processed file
    url(regex=r'^upload/$', view="upload_network", name="upload_network"),
    #Home Classification
    url(regex=r'^(.+)/$', view="network", name="network"),
    url(regex=r'^$', view="network", name="network"),
                       )