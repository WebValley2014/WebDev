from django.conf.urls import patterns, include, url

from django.contrib import admin
from .views import *

admin.autodiscover()

urlpatterns = patterns('classification.views',
    #Upload Pre-Processed file
    url(regex=r'^upload/$', view="upload_preProcessed", name="upload_preProcessed"),
    #Download
    url(regex=r'^download/(.+)/$', view="download", name="download"),
    #Option-PreAnalytics
    url(regex=r'^option/(.+)/$', view="option", name="option"),
    #Home Classification
    url(regex=r'^(.+)/$', view="classification", name="classification"),
    url(regex=r'^$', view="classification", name="classification"),

)
