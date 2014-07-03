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
    #LogoutPage
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    #UploadPage
    (r'^upload/$', "WebDev.views.upload"),
    #Contatact Test
    url(regex=r'^contact/$', view="WebDev.views.contact", name="contatti"),

    # Classification urls
    url(r'^class/', include('classification.urls')),
    # Preprocess urls
    url(r'^preproc/', include('preprocess.urls')),
    # Network urls
    url(r'^network/', include('network.urls')),
)
