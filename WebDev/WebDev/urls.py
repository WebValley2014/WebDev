from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'WebDev.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #Home page
    (r'^$', "WebDev.views.index"),
    #Login page
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    #User_login
    url(r'^upload/$', "WebDev.views.upload"),


)
