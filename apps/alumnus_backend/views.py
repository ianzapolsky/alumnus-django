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
def get_memberlist(request, memberlist_id):
    if request.method == 'GET':
        memberlist = get_object_or_404(MemberList, pk=memberlist_id)
        if memberlist.organization.owner != request.user: 
            return HttpResponse('Sorry, you do not own that MemberList.')
        response = {'members': serializers.serialize('json', memberlist.members.all())}
        return HttpResponse(json.dumps(response), content_type='appliction/json')

@login_required
def get_organization(request, organization_id):
    if request.method == 'GET':
        organization = get_object_or_404(Organization, pk=organization_id)
        if organization.owner != request.user: 
            return HttpResponse('Sorry, you do not own that Organization.')
        response = {'members': serializers.serialize('json', organization.get_members().all())}
        return HttpResponse(json.dumps(response), content_type='appliction/json')

@login_required
def organization_delete(request):
    """ Deletes the specified organization """
    if request.method == 'POST':
        organization_id  = request.POST.get('organization_id')
        organization = get_object_or_404(Organization, pk=organization_id) 
        if organization.owner != request.user:
            message = 'Sorry, you do not own this organization.'
            redirect = None
        else:
            organization.delete()
            message = 'Organization successfully deleted.' 
            redirect = '/'
        messages.add_message(request, messages.INFO, message)
        response = {'redirect': redirect} 
        return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
def memberlist_delete(request):
    """ Deletes the specified memberlist, assuming the user owns that memberlist """
    if request.method == 'POST':
        memberlist_id  = request.POST.get('memberlist_id')
        memberlist = get_object_or_404(MemberList, pk=memberlist_id) 
        organization = memberlist.organization
        if organization.owner != request.user:
            message = 'Sorry, you do not own this memberlist.'
            redirect = None
        else:
            memberlist.delete()
            message = 'MemberList successfully deleted.' 
            redirect = organization.get_memberlists_url()
        messages.add_message(request, messages.INFO, message)
        response = {'redirect': redirect} 
        return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
def member_delete(request):
    """ Deletes the specified member, assuming the user owns that member's organization """
    if request.method == 'POST':
        member_id  = request.POST.get('member_id')
        member = get_object_or_404(Member, pk=member_id) 
        organization = member.organization
        if organization.owner != request.user:
            message = 'Sorry, you do not own the organization this member is in.'
            redirect = None
        else:
            member.delete()
            message = 'Member successfully deleted.' 
            redirect = organization.get_members_url()
        messages.add_message(request, messages.INFO, message)
        response = {'redirect': redirect} 
        return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
def member_update_request(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '')
        member = get_object_or_404(Member, pk=member_id)
        if member.organization.owner != request.user:
            return HttpResponse('Sorry, you do not own that member.')
        context = { 
          'user': request.user,
          'member': member,
          'organization': member.organization,
          'site_name': settings.SITE_NAME
        }
        context = Context(context)
        text_content = get_template('emails/member_update_request.txt').render(context)
        html_content = get_template('emails/member_update_request.html').render(context)
        to = member.email
        reply_to = request.user.email
        subject, from_email = 'Member Update Request', settings.DEFAULT_FROM_EMAIL
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to], headers={'Reply-To': reply_to})
        msg.attach_alternative(html_content, 'text/html')
        successful = msg.send()
        if successful == 0:
            message = 'There was an error sending the email. Please try again.'
        else:
            message = 'Email successfully sent.'
        member.increment_times_requested()
        member.set_last_requested()
        messages.add_message(request, messages.INFO, message)
        response = {'successful': successful, 'redirect': member.get_absolute_url()}
        return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
def organization_send_mail(request):
    if request.method == 'POST':
        organization_id = request.POST.get('organization_id')
        organization = get_object_or_404(Organization, pk=organization_id)
        if organization.owner != request.user:
            return HttpResponse('Sorry, you do not own that organization.')

        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        text_content = message
        # Important to note here that we get an array from the client, so do not
        # need to cast "to" as an array later in our EmailMessage instantiation.
        to = json.loads(request.POST.get('recipients'))
        reply_to = request.user.email
        from_email = settings.DEFAULT_FROM_EMAIL
        msg = EmailMessage(subject, message, from_email, to, headers={'Reply-To': reply_to})
        successful = msg.send()
        if successful == 0:
            message = 'There was an error sending the email. Please try again.'
            redirect_url = organization.get_send_mail_url()
        else:
            message = 'Email successfully sent.'
            redirect_url = organization.get_absolute_url()
        # Stop adding messages from the API. This is counterintuitive, and 
        # confuses presentation logic with backend logic
        # messages.add_message(request, messages.INFO, message)
        response = {'successful': successful, 'redirect': redirect_url}
        return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
def member_send_mail(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        member = get_object_or_404(Member, pk=member_id)
        if member.organization.owner != request.user:
            return HttpResponse('Sorry, you do not own that member.')

        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        text_content = message
        to = member.email
        reply_to = request.user.email
        from_email = settings.DEFAULT_FROM_EMAIL
        msg = EmailMessage(subject, message, from_email, [to], headers={'Reply-To': reply_to})
        successful = msg.send()
        if successful == 0:
            message = 'There was an error sending the email. Please try again.'
            redirect_url = member.get_send_mail_url()
        else:
            message = 'Email successfully sent.'
            redirect_url = member.get_absolute_url()
        messages.add_message(request, messages.INFO, message)
        response = {'successful': successful, 'redirect': redirect_url}
        return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
def memberlist_send_mail(request):
    if request.method == 'POST':
        memberlist_id = request.POST.get('memberlist_id')
        memberlist = get_object_or_404(MemberList, pk=memberlist_id)
        if memberlist.organization.owner != request.user:
            return HttpResponse('Sorry, you do not own that memberlist.')

        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        text_content = message
        to = [member.email for member in memberlist.members.all()]
        reply_to = request.user.email
        from_email = settings.DEFAULT_FROM_EMAIL
        msg = EmailMessage(subject, message, from_email, to, headers={'Reply-To': reply_to})
        successful = msg.send()
        if successful == 0:
            message = 'There was an error sending the email. Please try again.'
            redirect_url = member.get_send_mail_url()
        else:
            message = 'Email successfully sent.'
            redirect_url = member.get_absolute_url()
        messages.add_message(request, messages.INFO, message)
        response = {'successful': successful, 'redirect': redirect_url}
        return HttpResponse(json.dumps(response), content_type='application/json')

