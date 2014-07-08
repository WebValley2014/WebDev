from django.conf.urls import patterns, include, url

from django.contrib import admin
from .views import *

admin.autodiscover()

urlpatterns = patterns('classification.views',
    #Upload Pre-Processed file
    url(regex=r'^upload/$', view="upload_preProcessed", name="class_upload"),
    url(regex=r'^step2/$', view='step2', name='step2'),
    #Download
    url(regex=r'^download/(.+)/$', view="download", name="download"),
    #Option-PreAnalytics
    url(regex=r'^option/(.+)/$', view="option", name="option"),

    url(regex=r'^delete/(?P<id>[0-9]+)/$', view="deleteFile", name="delete"),

    #Home Classification
    url(regex=r'^(.+)/$', view="classification", name="classification"),
    url(regex=r'^$', view="classification_redirect"),

)
