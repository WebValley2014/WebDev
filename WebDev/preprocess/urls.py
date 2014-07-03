from django.conf.urls import patterns, include, url

from django.contrib import admin
from .views import *
admin.autodiscover()

urlpatterns = patterns('preprocess.views',
                       )


