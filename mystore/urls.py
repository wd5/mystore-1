# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#from django.conf.urls.static import static
from mystore import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ajax/category/$', 'catalog.views.ajax_category'),
    url(r'^search/$', 'search.views.search'),
    url(r'^', include('catalog.urls')),
)

urlpatterns += staticfiles_urlpatterns()

handler404 = 'views.file_not_found_404'
