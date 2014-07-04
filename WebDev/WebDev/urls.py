from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'WebDev.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #Home page
    url(r'^$', "WebDev.views.index", name='index'),
    #Login page
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    #LogoutPage
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    #Contact
    url(r'^contact/$', "WebDev.views.contact", name='contact'),
    #About_us
    url(r'^about_us/$', "WebDev.views.about_us", name='about'),


    # Classification urls
    url(r'^class/', include('classification.urls')),
    # Preprocess urls
    url(r'^preproc/', include('preprocess.urls')),
    # Network urls
    url(r'^network/', include('network.urls')),
)
