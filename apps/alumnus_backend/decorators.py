import json
from functools import wraps

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from alumnus_backend.models import Organization, Member, MemberList

def ownership_required(function):
    def wrap(request, *args, **kwargs):
        try:
            organization = get_object_or_404(Organization, slug=kwargs['organization_slug'])
        except:
            pass
        try: 
            member = get_object_or_404(Member, slug=kwargs['member_slug'])
            organization = member.organization
        except:
            pass
        try:
            memberlist = get_object_or_404(MemberList, slug=kwargs['memberlist_slug'])
            organization = memberlist.organization
        except:
            pass

        if organization.owner != request.user:
            return HttpResponseRedirect('/account/permissions-error')
        return function(request, *args, **kwargs)

    return wrap

def access_required(function):
    def wrap(request, *args, **kwargs):
        try:
            organization = get_object_or_404(Organization, slug=kwargs['organization_slug'])
        except:
            pass
        try: 
            member = get_object_or_404(Member, slug=kwargs['member_slug'])
            organization = member.organization
        except:
            pass
        try:
            memberlist = get_object_or_404(MemberList, slug=kwargs['memberlist_slug'])
            organization = memberlist.organization
        except:
            pass

        if organization.owner != request.user and organization not in Organization.objects.filter(privileged_users__in=[request.user]):
            return HttpResponseRedirect('/account/permissions-error')
        return function(request, *args, **kwargs)
  
    return wrap

def ownership_required_ajax(function):
    def wrap(request, *args, **kwargs):
        if request.method == 'GET':
            try:
                organization = Organization.objects.get(pk=kwargs['organization_id'])
            except:
                pass
        if request.method == 'POST':      
            print 'hello'
            try:
                organization_id = request.POST.get('organization_id', '')
                organization = get_object_or_404(Organization, pk=organization_id)
            except:
                pass
            try:
                member_id = request.POST.get('member_id', '')
                member = get_object_or_404(Member, pk=member_id)
                organization = member.organization
            except:
                pass
            try:
                memberlist_id = request.POST.get('memberlist_id', '')
                memberlist = get_object_or_404(MemberList, pk=memberlist_id)
                organization = memberlist.organization
            except:
                pass

        if organization.owner != request.user:
            response = {'message': 'Sorry, you cannot perform this action because do not own this Organization.', 'error': True}
            return HttpResponse(json.dumps(response), content_type='application/json')
        return function(request, *args, **kwargs)

    return wrap
            
def access_required_ajax(function):
    def wrap(request, *args, **kwargs):
        if request.method == 'GET':
            try:
                organization = Organization.objects.get(pk=kwargs['organization_id'])
            except:
                pass
        if request.method == 'POST':      
            try:
                organization_id = request.POST.get('organization_id', '')
                organization = get_object_or_404(Organization, pk=organization_id)
            except:
                pass
            try:
                member_id = request.POST.get('member_id', '')
                member = get_object_or_404(Member, pk=member_id)
                organization = member.organization
            except:
                pass
            try:
                memberlist_id = request.POST.get('memberlist_id', '')
                memberlist = get_object_or_404(MemberList, pk=memberlist_id)
                organization = memberlist.organization
            except:
                pass

        if organization.owner != request.user and organization not in Organization.objects.filter(privileged_users__in=[request.user]):
            response = {'message': 'Sorry, you do not have access to this Organization.', 'error': True}
            return HttpResponse(json.dumps(response), content_type='application/json')
        return function(request, *args, **kwargs)

    return wrap
