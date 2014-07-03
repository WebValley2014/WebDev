from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import *

admin.autodiscover()

urlpatterns = patterns('preprocess.views',
    #Preprocess page
    #(r'$', 'preprocess'),
    url(regex='^launch/$', view=submit_celery, name='launch'),
    url(regex='^res/(.+)/$', view=get_results, name='res'),
)


