from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('preprocess.views',
    #Preprocess page
    url(regex=r'^preprocess/$', view="preprocess", name="preprocess"),
)


