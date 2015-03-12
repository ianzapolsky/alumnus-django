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
          'member': member,
          'site_name': settings.SITE_NAME
        }
        subject = request.POST.get('subject', 'Member Update Request')
        message = request.POST.get('message', '')
        from_name = request.POST.get('from', str(member.organization))
        context = Context(context)

        text_content = message + '\n\n' + get_template('emails/member_update_request.txt').render(context)
        to = member.email
        reply_to = request.user.email
        from_email = from_name + ' <' + settings.DEFAULT_FROM_EMAIL + '>'

        print from_email

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to], headers={'Reply-To': reply_to})
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
def member_send_mail(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        member = get_object_or_404(Member, pk=member_id)
        if member.organization.owner != request.user:
            return HttpResponse('Sorry, you do not own that member.')

        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        from_name = request.POST.get('from', str(member.organization))

        text_content = message
        to = member.email
        reply_to = request.user.email
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

@login_required
def group_send_mail(request):
    if request.method == 'POST':
        recipients = request.POST.getlist('recipients[]', '')
        organization = Member.objects.get(pk=request.POST.get('member_id')).organization

        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        from_name = request.POST.get('from', str(organization))

        text_content = message
        reply_to = request.user.email
        from_email = from_name + ' <' + settings.DEFAULT_FROM_EMAIL + '>'

        msg = EmailMessage(subject, message, from_email, recipients, headers={'Reply-To': reply_to})
        successful = msg.send()

        if successful == 0:
            message = 'There was an error sending the email. Please try again.'
        else:
            message = 'Email successfully sent.'
        response = {'successful': successful}
        return HttpResponse(json.dumps(response), content_type='application/json')
