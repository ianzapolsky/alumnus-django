import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import Context
from django.template.loader import get_template

from .decorators import ownership_required_ajax, access_required_ajax
from .models import Organization, Member, MemberList


@login_required
def get_organizations(request):
    """ Returns all of the requesting user's organizations """
    if request.method == 'GET':
        organizations = Organization.objects.filter(owner=request.user)
        return HttpResponse(organizations)


def user_exists(request):
    """ Returns whether or not the user exists """
    if request.method == 'POST':
        username = request.POST.get('username', '') 
        if len(User.objects.filter(username=username).all()) > 0:
            return HttpResponse(json.dumps({'exists': True}), content_type='application/json')
        return HttpResponse(json.dumps({'exists': False}), content_type='application/json')


def user_check_password(request):
    """ Returns whether or not the password matches the user """
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return HttpResponse(json.dumps({'valid': True}), content_type='application/json')
            return HttpResponse(json.dumps({'valid': False}), content_type='application/json')
        except:
            return HttpResponse(json.dumps({'valid': False}), content_type='application/json')


@login_required
@access_required_ajax
def get_memberlist(request, memberlist_id):
    if request.method == 'GET':
        memberlist = get_object_or_404(MemberList, pk=memberlist_id)
        response = {'members': serializers.serialize('json', memberlist.members.all())}
        return HttpResponse(json.dumps(response), content_type='appliction/json')


@login_required
@access_required_ajax
def get_organization(request, organization_id):
    if request.method == 'GET':
        organization = get_object_or_404(Organization, pk=organization_id)
        response = {'members': serializers.serialize('json', organization.get_members())}
        return HttpResponse(json.dumps(response), content_type='appliction/json')


@login_required
@ownership_required_ajax
def organization_delete(request):
    """ Deletes the specified organization """
    if request.method == 'POST':
        organization_id  = request.POST.get('organization_id')
        organization = get_object_or_404(Organization, pk=organization_id) 
        organization.delete()
        message = 'Organization successfully deleted.' 
        redirect = '/'
        messages.add_message(request, messages.INFO, message)
        response = {'redirect': redirect} 
        return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
@ownership_required_ajax
def organization_grant_access(request):
    """ Adds the specified User as a privileged User to the Organization """
    if request.method == 'POST':
        organization_id  = request.POST.get('organization_id')
        organization = get_object_or_404(Organization, pk=organization_id) 
        username = request.POST.get('username')

        try:
            user = User.objects.get(username=username)
        except:
            response = {'message': 'That user does not exist.', 'error': True}
            return HttpResponse(json.dumps(response), content_type='application/json')

        if organization.privileged_users.filter(username=user.username).exists():
            message = str(user) + ' has already been granted access to ' + str(organization) + '.' 
            error = True
        else:
            organization.privileged_users.add(user)
            message = str(user) + ' has been granted access to ' + str(organization) + '.' 
            error = False

        response = {'message': message, 'error': error}
        return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
@ownership_required_ajax
def organization_transfer_ownership(request):
    """ Changes the specified User to be the new owner of the Organization """
    if request.method == 'POST':
        organization_id  = request.POST.get('organization_id')
        organization = get_object_or_404(Organization, pk=organization_id) 
        username = request.POST.get('username')

        try:
            user = User.objects.get(username=username)
        except:
            response = {'message': 'That user does not exist.', 'error': True}
            return HttpResponse(json.dumps(response), content_type='application/json')
        if organization.owner == user:
            response = {'message': 'That user is already the owner of this Organization.', 'error': True}
            return HttpResponse(json.dumps(response), content_type='application/json')

        if organization.privileged_users.filter(username=user.username).exists():
            organization.privileged_users.remove(user)
        organization.owner = user
        if not organization.privileged_users.filter(username=request.user.username).exists():
            organization.privileged_users.add(request.user)
        organization.save()

        message = str(user) + ' has been made the new owner of ' + str(organization) + '. ' + str(request.user) + ' has been made a privileged user automatically.'
        messages.add_message(request, messages.INFO, message)
        response = {'message': message, 'error': False, 'redirect': organization.get_absolute_url()}
        return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
@ownership_required_ajax
def memberlist_delete(request):
    """ Deletes the specified memberlist, assuming the user owns that memberlist """
    if request.method == 'POST':
        memberlist_id  = request.POST.get('memberlist_id')
        memberlist = get_object_or_404(MemberList, pk=memberlist_id) 
        organization = memberlist.organization
        memberlist.delete()
        message = 'MemberList successfully deleted.' 
        error = False
        redirect = organization.get_memberlists_url()
        messages.add_message(request, messages.INFO, message)
        response = {'message': message, 'error': error, 'redirect': redirect} 
        return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
@ownership_required_ajax
def member_delete(request):
    """ Deletes the specified member, assuming the user owns that member's organization """
    if request.method == 'POST':
        member_id  = request.POST.get('member_id')
        member = get_object_or_404(Member, pk=member_id) 
        organization = member.organization
        member.delete()
        message = 'Member successfully deleted.' 
        redirect = organization.get_members_url()
        messages.add_message(request, messages.INFO, message)
        response = {'redirect': redirect} 
        return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
@access_required_ajax
def member_update_request(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '')
        member = get_object_or_404(Member, pk=member_id)

        context = { 
          'member': member,
          'site_name': settings.SITE_NAME
        }

        subject = request.POST.get('subject', 'Member Update Request')
        message = request.POST.get('message', '')
        from_name = request.POST.get('from', str(member.organization))
        context = Context(context)

        text_content = message + '\n\n' + get_template('emails/member_update_request.txt').render(context)
        to = member.email
        from_email = from_name + ' <' + settings.DEFAULT_FROM_EMAIL + '>'

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        successful = msg.send()

        if successful == 0:
            message = 'There was an error sending the email. Please try again.'
        else:
            message = 'Email successfully sent.'
        member.increment_times_requested()
        member.set_last_requested()
        response = {'successful': successful, 'redirect': member.get_absolute_url()}
        return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
@access_required_ajax
def member_send_mail(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        member = get_object_or_404(Member, pk=member_id)
    
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        from_name = request.POST.get('from', str(member.organization))
        from_address = request.POST.get('from_email', str(member.organization))

        text_content = message
        to = member.email
        reply_to = from_address
        from_email = from_name + ' <' + settings.DEFAULT_FROM_EMAIL + '>'

        msg = EmailMessage(subject, message, from_email, [to], headers={'Reply-To': reply_to})
        successful = msg.send()

        if successful == 0:
            message = 'There was an error sending the email. Please try again.'
            redirect_url = member.get_send_mail_url()
        else:
            message = 'Email successfully sent.'
            redirect_url = member.get_absolute_url()
        response = {'successful': successful, 'redirect': redirect_url}
        return HttpResponse(json.dumps(response), content_type='application/json')

