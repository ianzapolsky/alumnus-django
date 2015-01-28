from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm 
from .views import CustomUserCreateView


# Website URLs
urlpatterns = patterns('',

    # Marketing
    url(r'^contact/$', TemplateView.as_view(template_name='marketing/contact.html')),
    url(r'^about/$', TemplateView.as_view(template_name='marketing/about.html')),

    # User Management
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}), 
    url(r'^register/$', CustomUserCreateView.as_view()),
    url(r'^activate/(?P<token>[-\w\d]+)/$', 'website.views.user_activate'),

    # Home
    url(r'^$', 'website.views.organizations'),

    # Organizations
    url(r'^organizations/$', 'website.views.organizations'),
    url(r'^organizations/(?P<organization_id>\d+)/$', 'website.views.organization_detail'),
    url(r'^organizations/create/$', 'website.views.organization_create'),

    # Members
    url(r'^organizations/(?P<organization_id>\d+)/members/$', 'website.views.members'),
    url(r'^members/(?P<member_id>\d+)/$', 'website.views.member_detail'),
    url(r'^organizations/(?P<organization_id>\d+)/members/create/$', 'website.views.member_create'),
    url(r'^organizations/(?P<organization_id>\d+)/members/import/$', 'website.views.member_import'),
    url(r'^members/(?P<member_id>\d+)/update/$', 'website.views.member_update'),
    # Public member update view, visible to only those with a valid AccessToken
    url(r'^members/(?P<member_id>\d+)/update/(?P<token>[-\w\d]+)/$', 'website.views.member_update_public'),

    # MemberLists
    url(r'^organizations/(?P<organization_id>\d+)/memberlists/$', 'website.views.memberlists'),
    url(r'^memberlists/(?P<memberlist_id>\d+)/$', 'website.views.memberlist_detail'),
    url(r'^organizations/(?P<organization_id>\d+)/memberlists/create/$', 'website.views.memberlist_create'),
    url(r'^memberlists/(?P<memberlist_id>\d+)/update/$', 'website.views.memberlist_update'),
  
    # Send email
    url(r'^organizations/(?P<organization_id>\d+)/send-mail/$', 'website.views.organization_send_mail'),
    url(r'^members/(?P<member_id>\d+)/send-mail/$', 'website.views.member_send_mail'),
    url(r'^memberlists/(?P<memberlist_id>\d+)/send-mail/$', 'website.views.memberlist_send_mail'), 

)
