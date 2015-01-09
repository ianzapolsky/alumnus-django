from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from alumnus_backend.models import Organization, Member, MemberList, AccessToken
from .forms import OrganizationForm, MemberForm, MemberListForm

@login_required
def organizations(request):
    context = {'user': request.user}
    context['organizations'] = Organization.objects.filter(owner=request.user)
    return render(request, 'organization_list.html', context)

@login_required
def organization_detail(request, organization_id):
    context = {'user': request.user}
    organization = Organization.objects.get(pk=organization_id)
    if organization.owner != request.user:
        return HttpResponse('Sorry, you do not own that organization.')
    context['organization'] = organization
    return render(request, 'organization_detail.html', context)

@login_required
def members(request, organization_id):
    context = {'user': request.user}
    organization = Organization.objects.get(pk=organization_id)
    if organization.owner != request.user:
        return HttpResponse('Sorry, you do not own that organization.')
    context['organization'] = organization
    context['members'] = Member.objects.filter(organization=organization)
    return render(request, 'member_list.html', context)

@login_required
def member_detail(request, member_id):
    context = {'user': request.user}
    member = Member.objects.get(pk=member_id)
    if member.organization.owner != request.user:
        return HttpResponse('Sorry, you do not have rights to this member.')
    context['member'] = member
    return render(request, 'member_detail.html', context)

@login_required
def create_organization(request):
    context = {'user': request.user}
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.owner = request.user
            organization.save()
            return redirect('/')
    else:
        context['form'] = OrganizationForm()    
    return render(request, 'registration/register.html', context)

@login_required
def create_member(request, organization_id):
    context = {'user': request.user}
    organization = Organization.objects.get(pk=organization_id)
    if organization.owner != request.user:
        return HttpResponse('Sorry, you do not own that organization.')
    context['organization'] = organization
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.organization = organization
            member.save()
            return redirect(organization.get_members_url())
    else:
        context['form'] = MemberForm()    
    return render(request, 'registration/register.html', context)

@login_required
def member_update(request, member_id):
    context = {'user': request.user}
    member = get_object_or_404(Member, pk=member_id)
    organization = member.organization
    if organization.owner != request.user:
        return HttpResponse('Sorry, you do not have rights to this member.')
    context['member'] = member
    context['organization'] = organization
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            context['form'] = form
            return render(request, 'registration/register.html', context)
    else:
        context['form'] = MemberForm(instance=member)
        return render(request, 'registration/register.html', context)

"""
This URL is does not require login because it needs to be open to users
without an account accessing the URL via a one-time expiring AccessToken
"""
def member_update_public(request, member_id, token):
    if request.method == 'GET':
        access_tokens = AccessToken.objects.filter(token=token, used=False)
        if access_tokens:
            access_token = access_tokens[0]
            access_token.used = True
            access_token.save()
        else:
            return HttpResponse('Sorry, that is an invalid access token.')
    member = get_object_or_404(Member, pk=member_id)
    context = {'member': member}
    context['organization'] = member.organization
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            context['form'] = form
            return render(request, 'registration/register.html', context)
    else:
        context['form'] = MemberForm(instance=member)
        return render(request, 'registration/register.html', context)

@login_required
def member_update_request(request, member_id):
    context = {'user': request.user}
    member = get_object_or_404(Member, pk=member_id)
    context['member'] = member
    context['organization'] = member.organization
    return render(request, 'emails/member_update_request.html', context)
    

@login_required
def memberlists(request, organization_id):
    context = {'user': request.user}
    organization = get_object_or_404(Organization, pk=organization_id)
    if organization.owner != request.user:
        return HttpResponse('Sorry, you do not own that organization.')
    context['organization'] = organization
    context['memberlists'] = MemberList.objects.filter(organization=organization)
    return render(request, 'memberlist_list.html', context)

@login_required
def memberlist_detail(request, memberlist_id):
    context = {'user': request.user}
    memberlist = get_object_or_404(MemberList, pk=memberlist_id)
    organization = memberlist.organization
    if organization.owner != request.user:
        return HttpResponse('Sorry, you do not own that memberlist.')
    context['organization'] = organization
    context['memberlist'] = memberlist
    return render(request, 'memberlist_detail.html', context)

@login_required
def create_memberlist(request, organization_id):
    context = {'user': request.user}
    organization = get_object_or_404(Organization, pk=organization_id)
    if organization.owner != request.user:
        return HttpResponse('Sorry, you do not own that organization.')
    context['organization'] = organization
    if request.method == 'POST':
        form = MemberListForm(organization, request.POST)
        if form.is_valid():
            memberlist = form.save(commit=False)
            memberlist.organization = organization
            memberlist.save()
            form.save_m2m()
            return redirect('/')
    else:
        context['form'] = MemberListForm(organization)    
    return render(request, 'registration/register.html', context)
    
@login_required
def memberlist_update(request, memberlist_id):
    memberlist = get_object_or_404(MemberList, pk=memberlist_id)
    organization = memberlist.organization
    if organization.owner != request.user:
        return HttpResponse('Sorry, you do not own that memberlist')
    context = {'memberlist': memberlist}
    if request.method == 'POST':
        form = MemberListForm(organization, request.POST, instance=memberlist)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            context['form'] = form
            return render(request, 'registration/register.html', context)
    else:
        context['form'] = MemberListForm(organization, instance=memberlist)
        return render(request, 'registration/register.html', context)

