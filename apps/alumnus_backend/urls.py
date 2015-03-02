from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


# Backend URLs
urlpatterns = patterns('',

    # Users
    url(r'^users/exists/$', 'alumnus_backend.views.user_exists'),
    url(r'^users/check-password/$', 'alumnus_backend.views.user_check_password'),

    # Organizations
    url(r'^organizations/$', 'alumnus_backend.views.get_organizations'),
    url(r'^organizations/(?P<organization_id>\d+)/$', 'alumnus_backend.views.get_organization'),
    url(r'^organizations/delete/$', 'alumnus_backend.views.organization_delete'),

    # Members
    url(r'^members/delete/$', 'alumnus_backend.views.member_delete'),
    url(r'^members/request-update/$', 'alumnus_backend.views.member_update_request'),

    # MemberLists
    url(r'^memberlists/(?P<memberlist_id>\d+)/$', 'alumnus_backend.views.get_memberlist'),
    url(r'^memberlists/delete/$', 'alumnus_backend.views.memberlist_delete'),
    
    # Send mail
    url(r'^members/send-mail/$', 'alumnus_backend.views.member_send_mail'),

)
