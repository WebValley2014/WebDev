from django.conf.urls import patterns, include, url
from django.conf import settings
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
    #FARINA
    url(r'^results/3D_graph/$', "WebDev.views.graph_3D", name='3Dgraph'),
    url(r'^results/3D_graph_oculus/$', "WebDev.views.graph_oculus_3D", name='3Dgraph_oculus'),
	url(r'^results/tree_graph/$', "WebDev.views.tree_graph", name='tree_graph'),
    #STEFANO
    url(r'^results/2D_graph/$', "WebDev.views.graph_2d", name='2Dgraph'),
	#LEONESSI
	url(r'^results/network/$', "WebDev.views.network", name='network_graph'),

    # Classification urls
    url(r'^class/', include('classification.urls')),
    # Preprocess urls
    url(r'^preproc/', include('preprocess.urls')),
    # Network urls
    url(r'^network/', include('network.urls')),

    #media
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, }),
)
