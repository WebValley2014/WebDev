from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import *

admin.autodiscover()

urlpatterns = patterns('preprocess.views',
    #Processing
    url(regex='^processing/(.+)/$', view='processing', name='preproc_processing'),
    #Celery
    url(regex='^celery/(.+)/$', view="celery", name="preproc_celery"),
    #Upload page
    url(regex='^upload/$', view="upload", name='preproc_upload'),
    #In processing page
    url(regex='^(.+)/$', view="get_results", name='preproc_get_result'),
    #Processing root (redirect to upload)
    url(regex=r'^$', view="preproc_preprocess_redirect"),
)


