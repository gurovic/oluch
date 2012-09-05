from django.conf.urls import patterns, include, url
from oluch import settings
from django.contrib.auth import login

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'oluch.views.index', name='index'),
    #url(r'member^$', 'oluch.views.member', name='member'),
    url(r'^login$', 'django.contrib.auth.views.login', name='login'),
    url(r'^choose_page$', 'oluch.views.choose_page', name='choose_page'),
    url(r'^register$', 'oluch.views.register', name='register'),
    url(r'^logout$', 'oluch.views.logout_user', name='logout'),
    url(r'^statistics$', 'oluch.views.statistics', name='statistics'),
    url(r'^results$', 'oluch.views.results', name='results'),
    url(r'^submit$', 'oluch.views.submit', name='submit'),
    url(r'^check/(?P<time>[12])../(?P<id>\d+)$', 'oluch.views.check', name='check'),
    url(r'^rate/(?P<submit_id>\d+)/(?P<time>[12])/(?P<mark>\d+)$', 'oluch.views.rate', name='rate'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),

)
