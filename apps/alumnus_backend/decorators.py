import json
from functools import wraps

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from alumnus_backend.models import Organization, Member

def ownership_required(function):
    def wrap(request, *args, **kwargs):
        organization = get_object_or_404(Organization, slug=kwargs['organization_slug'])
        if organization.owner != request.user:
            return HttpResponse('Sorry, you do not own this Organization.')
        return function(request, *args, **kwargs)

    return wrap

def access_required(function):
    def wrap(request, *args, **kwargs):
        organization = get_object_or_404(Organization, slug=kwargs['organization_slug'])
        if organization.owner != request.user and organization not in Organization.objects.filter(privileged_users__in=[request.user]):
            return HttpResponse('Sorry, you do not have access to this Organization.')
        return function(request, *args, **kwargs)
  
    return wrap

def ownership_required_ajax(function):
    def wrap(request, *args, **kwargs):
        if request.method == 'POST':      
            member_id = request.POST.get('member_id', '')
            member = get_object_or_404(Member, pk=member_id)
            if member.organization.owner != request.user:
                response = {'message': 'Sorry, you do not own this Organization.', 'error': True}
                return HttpResponse(json.dumps(response), content_type='application/json')
        return function(request, *args, **kwargs)

    return wrap
            
def access_required_ajax(function):
    def wrap(request, *args, **kwargs):
        if request.method == 'POST':      
            member_id = request.POST.get('member_id', '')
            member = get_object_or_404(Member, pk=member_id)
            if member.organization.owner != request.user and member.organization not in Organization.objects.filter(privileged_users__in=[request.user]):
                response = {'message': 'Sorry, you do not have access to this Organization.', 'error': True}
                return HttpResponse(json.dumps(response), content_type='application/json')
        return function(request, *args, **kwargs)

    return wrap
            
