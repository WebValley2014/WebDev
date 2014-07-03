from django.conf.urls import patterns, include, url

from django.contrib import admin
from .views import *

admin.autodiscover()

urlpatterns = patterns('classification.views',
    #Upload of pre-processed files
    url(regex=r'^classification/$', view="classification", name="classification"),
)
