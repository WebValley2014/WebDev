from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import *

admin.autodiscover()

urlpatterns = patterns('preprocess.views',
    #Celery
    url(regex='^celery/(.+)/$', view="celery", name="celery"),
    #Upload page
    url(regex='^upload/$', view="upload", name='upload'),
    #In processing page
    url(regex='^(.+)/$', view="get_results", name='get_result'),
    #Processing root (redirect to upload)
    url(regex=r'^$', view="preprocess_redirect"),
)


