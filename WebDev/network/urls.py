from django.conf.urls import patterns, include, url

from django.contrib import admin
from .views import *
admin.autodiscover()


urlpatterns = patterns('network.views',

    url(regex=r'^show_results/(.+)/$', view="show_results", name="show_results_net"),
    #Upload Pre-Processed file
    url(regex=r'^upload/$', view="upload_network", name="network_upload"),
    url(regex=r'^start_network/$', view='start_network', name='start_network'),
    #Home Classification
    #url(regex=r'^celery/(.+)/$', view='start_network', name='start_network'),

    url(regex=r'^delete/(.+)/(.+)/(.+)/(.+)/(.+)/(.+)/$', view="deleteFile", name="delete"),
    #Processing
    url(regex='^processing_finish/(.+)/$', view='processing_finish', name='processing_finish'),
    url(regex='^processing/(.+)/$', view='processing', name='processing'),
    url(regex=r'^option/(.+)/$', view="option", name="option"),
    #url(regex='^results/$', view='showResults', name='showResults'),

    url(regex=r'^(.+)/$', view="network", name="network"),
    url(regex=r'^$', view="network_redirect", name="network"),
    )