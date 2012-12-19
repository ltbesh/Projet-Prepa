from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^index/$', 'QCM.views.index'),
	url(r'^qcm/$', 'QCM.views.qcm'),
	url(r'^profil/$', 'QCM.views.index'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^register/$', 'QCM.views.register'),
    # Examples:
    # url(r'^$', 'projetprepa.views.home', name='home'),
    # url(r'^projetprepa/', include('projetprepa.foo.urls')),

    # Uncomment th admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
