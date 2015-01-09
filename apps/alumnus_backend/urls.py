from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


# Backend URLs
urlpatterns = patterns('',

    # Users
    url(r'^users/$', 'alumnus_backend.views.create_user'),

    # Organizations
    url(r'^organizations/$', 'alumnus_backend.views.get_organizations'),
    

)
