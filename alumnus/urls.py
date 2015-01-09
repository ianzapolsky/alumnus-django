from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    # Website
    url(r'^',       include('website.urls')),

    # Backend
    url(r'^api/',  include('alumnus_backend.urls')),

    # Admin
    url(r'^admin/', include(admin.site.urls)),

)
