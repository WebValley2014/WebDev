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

    url(regex=r'^delete/(.+)/(.+)/$', view="deleteFile", name="delete"),

    url(regex=r'^processing/(.+)/$', view="learning_loading", name="learning_loading"),



    #Home Classification
    url(regex=r'^(.+)/$', view="classification", name="classification"),
    url(regex=r'^$', view="classification_redirect"),

)
