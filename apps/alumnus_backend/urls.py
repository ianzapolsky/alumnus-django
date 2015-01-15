from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


# Backend URLs
urlpatterns = patterns('',

    # Users
    url(r'^users/$', 'alumnus_backend.views.create_user'),

    # Organizations
    url(r'^organizations/$', 'alumnus_backend.views.get_organizations'),

    # Members
    url(r'^members/delete/$', 'alumnus_backend.views.member_delete'),
    url(r'^members/request-update/$', 'alumnus_backend.views.member_update_request'),
    url(r'^members/send-mail/$', 'alumnus_backend.views.member_send_mail'),
    
    # Send mail
    url(r'^memberlists/send-mail/$', 'alumnus_backend.views.memberlist_send_mail'),

)
