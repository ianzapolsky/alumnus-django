import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import CreateView
from django.utils import timezone

from alumnus_backend.models import Organization, Member, MemberList, AccessToken, AuthenticationToken
from .forms import CustomUserCreationForm, OrganizationForm, MemberForm, MemberListForm, MemberImportForm
from .parser import ExcelParser


""" User views """
def user_activate(request, token):
    token_obj = get_object_or_404(AuthenticationToken, used=False, token=token)
    if token_obj.created > timezone.now() - datetime.timedelta(hours=settings.TOKEN_LIFETIME):
        user = token_obj.user
        user.is_active = True
        user.save()
        token_obj.used = True
        token_obj.save()
        messages.add_message(request, messages.INFO, 'Your account has been activated.')
        return redirect('/')
    else:
        messages.add_message(request, messages.INFO, 'Your activation token has expired.')
        """
        delete user model here?
        """
        return redirect('/')

class CustomUserCreateView(CreateView):

    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = '/'

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, 'Your account has been created. Please check your email for an activation link.')
        return super(CustomUserCreateView, self).form_valid(form)

""" Organization views """
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
def organization_create(request):
    context = {'user': request.user}
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        context['form'] = form
        if form.is_valid():
            organization = form.save(commit=False)
            organization.owner = request.user
            organization.save()
            messages.add_message(request, messages.INFO, 'Organization successfully created.')
            return redirect('/')
    else:
        context['form'] = OrganizationForm()    
    return render(request, 'generic/form.html', context)

@login_required
def organization_send_mail(request, organization_id):
    context = {'user': request.user}
    organization = get_object_or_404(Organization, pk=organization_id)
    if organization.owner != request.user:
        return HttpResponse('Sorry, you do not own this memberlist')
    context['organization'] = organization
    context['members'] = organization.get_members()
    return render(request, 'forms/organization_send_mail.html', context)

""" Member views """
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
    member = get_object_or_404(Member, pk=member_id)
    if member.organization.owner != request.user:
        return HttpResponse('Sorry, you do not have rights to this member.')
    context['member'] = member
    context['organization'] = member.organization
    return render(request, 'member_detail.html', context)

@login_required
def member_create(request, organization_id):
    context = {'user': request.user}
    organization = get_object_or_404(Organization, pk=organization_id)
    if organization.owner != request.user:
        return HttpResponse('Sorry, you do not own that organization.')
    context['organization'] = organization
    if request.method == 'POST':
        form = MemberForm(request.POST)
        fields = list(form)
        context['form_personal'] = fields[:4] 
        context['form_work'] = fields[4:]
        context['form'] = form
        if form.is_valid():
            member = form.save(commit=False)
            member.organization = organization
            member.save()
            messages.add_message(request, messages.INFO, 'Member successfully created.')
            return redirect(organization.get_members_url())
    else:
        context['form'] = MemberForm()    
        fields = list(context['form'])
        context['form_personal'] = fields[:4]
        context['form_work'] = fields[4:]
    return render(request, 'forms/member_create.html', context)

@login_required
def member_update(request, member_id):
    context = {'user': request.user}
    member = get_object_or_404(Member, pk=member_id)
    organization = member.organization
    if organization.owner != request.user:
        return HttpResponse('Sorry, you do not have rights to update this member.')
    context['member'] = member
    context['organization'] = organization
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        fields = list(form)
        context['form_personal'] = fields[:4] 
        context['form_work'] = fields[4:]
        context['form'] = form
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Member successfully updated.')
            return redirect(member.get_absolute_url())
    else:
        context['form'] = MemberForm(instance=member)
        fields = list(context['form'])
        context['form_personal'] = fields[:4] 
        context['form_work'] = fields[4:]
    return render(request, 'forms/member_create.html', context)

"""
This URL is does not require login because it needs to be open to users
without an account accessing the URL via a one-time expiring AccessToken
"""
def member_update_public(request, member_id, token):
    # Check that the access_token is not expired
    access_token = get_object_or_404(AccessToken, used=False, token=token)
    if access_token.created > timezone.now() - datetime.timedelta(hours=settings.TOKEN_LIFETIME):
        pass
        """
        Not necessarily appropriate to invalidate an AccessToken after first use.
        Imagine use case where the Member refreshes page, or starts the form but comes back to it later.
        AccessToken should remain valid for the entirety of its lifetime.
        access_token.used = True
        access_token.save()
        """
    else:
        return HttpResponse('Sorry, that is an invalid access token.')

    member = get_object_or_404(Member, pk=member_id)
    context = {'member': member}
    context['organization'] = member.organization
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        fields = list(form)
        context['form_personal'] = fields[:4] 
        context['form_work'] = fields[4:]
        context['form'] = form
        if form.is_valid():
            form.save()
            return redirect('/thanks')
        else:
            context['form'] = form
            return render(request, 'forms/member_create.html', context)
    else:
        context['form'] = MemberForm(instance=member)
        fields = list(context['form'])
        context['form_personal'] = fields[:4] 
        context['form_work'] = fields[4:]
        return render(request, 'forms/member_create.html', context)

@login_required
def member_send_mail(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    organization = member.organization
    if organization.owner != request.user:
        return HttpResponse('Sorry, you do not own this memberlist')
    context = {'member': member}
    context['organization'] = organization
    return render(request, 'forms/member_send_mail.html', context)

@login_required
def member_import(request, organization_id):
    context = {'user': request.user}
    organization = get_object_or_404(Organization, pk=organization_id)
    if organization.owner != request.user:
        return HttpResponse('Sorry, you do not own that organization.')
    context['organization'] = organization
    if request.method == 'POST':
        form = MemberImportForm(request.POST, request.FILES)
        if form.is_valid():
            parser = ExcelParser(request.FILES['file'], organization)
            parser.parse()
            messages.add_message(request, messages.INFO, 'Members successfully imported.')
            return redirect(organization.get_members_url())
        else:
            context['errors'] = form.errors
    else:
        form = MemberImportForm()
    context['form'] = form
    return render(request, 'forms/member_import.html', context)
        
""" MemberList views """
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
def memberlist_create(request, organization_id):
    context = {'user': request.user}
    organization = get_object_or_404(Organization, pk=organization_id)
    if organization.owner != request.user:
        return HttpResponse('Sorry, you do not own that organization.')
    context['organization'] = organization
    if request.method == 'POST':
        form = MemberListForm(organization, request.POST)
        context['form'] = form
        if form.is_valid():
            memberlist = form.save(commit=False)
            memberlist.organization = organization
            memberlist.save()
            form.save_m2m()
            messages.add_message(request, messages.INFO, 'MemberList successfully created.')
            return redirect('/')
    else:
        context['form'] = MemberListForm(organization)    
    return render(request, 'forms/memberlist_create.html', context)
    
@login_required
def memberlist_update(request, memberlist_id):
    memberlist = get_object_or_404(MemberList, pk=memberlist_id)
    organization = memberlist.organization
    if organization.owner != request.user:
        return HttpResponse('Sorry, you do not own that memberlist')
    context = {'memberlist': memberlist}
    context['organization'] = organization
    if request.method == 'POST':
        form = MemberListForm(organization, request.POST, instance=memberlist)
        context['form'] = form
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'MemberList successfully updated.')
            return redirect(organization.get_memberlists_url())
    else:
        context['form'] = MemberListForm(organization, instance=memberlist)
    return render(request, 'forms/memberlist_create.html', context)

@login_required
def memberlist_send_mail(request, memberlist_id):
    memberlist = get_object_or_404(MemberList, pk=memberlist_id)
    organization = memberlist.organization
    if organization.owner != request.user:
        return HttpResponse('Sorry, you do not own this memberlist')
    context = {'memberlist': memberlist}
    context['organization'] = organization
    return render(request, 'forms/memberlist_send_mail.html', context)

