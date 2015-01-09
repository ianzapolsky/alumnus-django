from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm 


# Website URLs
urlpatterns = patterns('',

    # User Management
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}), 
    url(r'^register/$', CreateView.as_view(
        template_name='registration/register.html',
        form_class=CustomUserCreationForm,
        success_url='/'
    )),

    # Home
    url(r'^$', 'website.views.organizations'),

    # Organizations
    url(r'^organizations/$', 'website.views.organizations'),
    url(r'^organizations/(?P<organization_id>\d+)/$', 'website.views.organization_detail'),
    url(r'^organizations/create/$', 'website.views.create_organization'),

    # Members
    url(r'^organizations/(?P<organization_id>\d+)/members/$', 'website.views.members'),
    url(r'^members/(?P<member_id>\d+)/$', 'website.views.member_detail'),
    url(r'^organizations/(?P<organization_id>\d+)/members/create/$', 'website.views.create_member'),
    url(r'^members/(?P<member_id>\d+)/update/$', 'website.views.member_update'),
    url(r'^members/(?P<member_id>\d+)/update-request/$', 'website.views.member_update_request'),

    # Public member update view, visible to only those with a valid AccessToken
    url(r'^members/(?P<member_id>\d+)/update/(?P<token>[-\w\d]+)/$', 'website.views.member_update_public'),

    # MemberLists
    url(r'^organizations/(?P<organization_id>\d+)/memberlists/$', 'website.views.memberlists'),
    url(r'^memberlists/(?P<memberlist_id>\d+)/$', 'website.views.memberlist_detail'),
    url(r'^memberlists/(?P<memberlist_id>\d+)/update$', 'website.views.memberlist_update'),
    url(r'^organizations/(?P<organization_id>\d+)/memberlists/create/$', 'website.views.create_memberlist'),
  
    
    # Send email
    

)
