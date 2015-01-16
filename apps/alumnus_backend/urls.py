from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


# Backend URLs
urlpatterns = patterns('',

    # Users
    url(r'^users/exists/$', 'alumnus_backend.views.user_exists'),
    url(r'^users/check-password/$', 'alumnus_backend.views.user_check_password'),

    # Organizations
    url(r'^organizations/$', 'alumnus_backend.views.get_organizations'),

    # Members
    url(r'^members/delete/$', 'alumnus_backend.views.member_delete'),
    url(r'^members/request-update/$', 'alumnus_backend.views.member_update_request'),

    # MemberLists
    url(r'^memberlists/(?P<memberlist_id>\d+)/$', 'alumnus_backend.views.get_memberlist'),
    
    # Send mail
    url(r'^organizations/send-mail/$', 'alumnus_backend.views.organization_send_mail'),
    url(r'^members/send-mail/$', 'alumnus_backend.views.member_send_mail'),
    url(r'^memberlists/send-mail/$', 'alumnus_backend.views.memberlist_send_mail'),

)
