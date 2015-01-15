import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import Context
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from .models import Organization, Member, MemberList


def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username, email, password)
        user.save()
        return HttpResponse(user)

@login_required
def get_organizations(request):
    """ Returns all of the requesting user's organizations """
    if request.method == 'GET':
        organizations = Organization.objects.filter(owner=request.user)
        return HttpResponse(organizations)

@login_required
def member_delete(request):
    """ Deletes the specified member, assuming the user owns that member's organization """
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        member = get_object_or_404(Member, pk=member_id) 
        organization = member.organization
        if organization.owner != request.user:
            msg = 'Sorry, you do not own the organization this member is in.'
        else:
            member.delete()
            msg = 'Member successfully deleted.' 
        messages.add_message(request, messages.INFO, 'Member successfully deleted')
        response = {'message': msg, 'redirect': organization.get_members_url()} 
        return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
def organization_delete(request):
    """ Deletes the specified organization, assuming the user owns that organization """
    if request.method == 'POST':
        organization_id = request.POST.get('organization_id')
        organization = get_object_or_404(Organization, pk=organization_id)
        if organization.owner != request.user:
            msg = 'Sorry, you do not own that organization.'
        else:
            organization.delete()
            msg = 'Organization successfully deleted.'
        response = {'message': msg} 
        return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
def member_update_request(request):
    if request.method == 'POST':
        context = {'user': request.user}
        member_id = request.POST.get('member_id', '')
        member = get_object_or_404(Member, pk=member_id)
        if member.organization.owner != request.user:
            return HttpResponse('Sorry, you do not own that member.')
        context['member'] = member
        context['organization'] = member.organization
        context = Context(context)

        text_content = get_template('emails/member_update_request.txt').render(context)
        html_content = get_template('emails/member_update_request.html').render(context)
        
        to = member.email
        reply_to = request.user.email
          
        subject, from_email = 'Member Update Request', settings.DEFAULT_FROM_EMAIL
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to], headers={'Reply-To': reply_to})
        msg.attach_alternative(html_content, 'text/html')
        successful = msg.send()
        response = {'successful': successful}
        return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
def member_send_mail(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        member = get_object_or_404(Member, pk=member_id)
        if member.organization.owner != request.user:
            return HttpResponse('Sorry, you do not own that member.')
        text_content = message

        to = member.email
        reply_to = request.user.email
        from_email = settings.DEFAULT_FROM_EMAIL

        msg = EmailMessage(subject, message, from_email, [to], headers={'Reply-To': reply_to})
        successful = msg.send()
        response = {'successful': successful}
        return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
def memberlist_send_mail(request):
    if request.method == 'POST':
        memberlist_id = request.POST.get('memberlist_id')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        memberlist = get_object_or_404(MemberList, pk=memberlist_id)
        if memberlist.organization.owner != request.user:
            return HttpResponse('Sorry, you do not own that memberlist.')
        text_content = message

        to = [member.email for member in memberlist.members.all()]
        reply_to = request.user.email
        from_email = settings.DEFAULT_FROM_EMAIL

        msg = EmailMessage(subject, message, from_email, to, headers={'Reply-To': reply_to})
        successful = msg.send()
        response = {'successful': successful}
        return HttpResponse(json.dumps(response), content_type='application/json')
