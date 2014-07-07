from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import *

admin.autodiscover()

urlpatterns = patterns('preprocess.views',
    #Delete File
    url(regex='^delete/(.+)/(.+)/$', view='deleteFile', name='file_delete'),
    #Processing
    url(regex='^processing/(.+)/(.+)/$', view='processing_finish', name='processing_finish'),
    url(regex='^processing/(.+)/$', view='processing', name='processing'),
    #Celery
    url(regex='^celery/(.+)/([0-1]{1})/$', view="start_preprocess", name="celery"),
    url(regex='^celery/(.+)/$', view="start_preprocess", name="celery"),
    #Upload page
    url(regex='^upload/$', view="upload", name='preproc_upload'),
    #In processing page
    url(regex='^(.+)/$', view="get_results", name='get_result'),
    #Processing root (redirect to upload)
    url(regex=r'^$', view="preprocess_redirect", name='redirect_preproc'),
)


