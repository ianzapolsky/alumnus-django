import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from localflavor.us.us_states import STATE_CHOICES

from .choices import *

class Organization(models.Model):

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User)
    slug = models.SlugField(unique=True)
    uuid = models.CharField(max_length=100, unique=True, default=uuid.uuid1)
    privileged_users = models.ManyToManyField(User, related_name='privileged_users')

    def __unicode__(self):
        return self.name

    def get_members(self):
        return Member.objects.filter(organization=self).all()

    def get_privileged_users(self):
        return self.privileged_users.all()

    def get_absolute_url(self):
        return '/organizations/' + self.slug
  
    def get_update_url(self):
        return self.get_absolute_url() + '/update'
  
    def get_members_url(self):
        return self.get_absolute_url() + '/members'

    def get_create_member_url(self):
        return self.get_members_url() + '/create'

    def get_import_member_url(self):
        return self.get_members_url() + '/import'

    def get_export_member_url(self):
        return self.get_members_url() + '/export'

    def get_memberlists_url(self):
        return self.get_absolute_url() + '/memberlists'
  
    def get_create_memberlist_url(self):
        return self.get_memberlists_url() + '/create'

    def get_send_mail_url(self):
        return self.get_absolute_url() + '/send-mail'

    def get_grant_access_url(self):
        return self.get_absolute_url() + '/grant-access'

    class Meta:
        ordering = ['name']


class Member(models.Model):

    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
    organization = models.ForeignKey(Organization)
    uuid = models.CharField(max_length=100, unique=True, default=uuid.uuid1)
    slug = models.SlugField(unique=True)
    participant_type = models.CharField(max_length=100, choices=PARTICIPATION_CHOICES, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    graduation_year = models.CharField(max_length=4, choices=YEAR_CHOICES, blank=True)
    school = models.CharField(max_length=10, choices=SCHOOL_CHOICES, blank=True)
    industry = models.CharField(max_length=100, choices=INDUSTRY_CHOICES, blank=True)
    company = models.CharField(max_length=100, blank=True)
    current_state = models.CharField(max_length=50, choices=STATE_CHOICES, blank=True)
    times_requested = models.IntegerField(default=0)
    times_completed = models.IntegerField(default=0)
    last_requested = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.firstname + ' ' + self.lastname

    def get_absolute_url(self):
        return '/members/' + self.slug

    def get_update_url(self):
        return self.get_absolute_url() + '/update'

    def get_update_request_url(self):
        return self.get_absolute_url() + '/update-request'

    def get_send_mail_url(self):
        return self.get_absolute_url() + '/send-mail'

    def get_public_update_url(self):
        # Create a new AccessToken every time this function is called
        token = AccessToken()
        token.save()
        return self.get_update_url() + '/' + str(token)
  
    def increment_times_requested(self):
        self.times_requested = self.times_requested + 1
        self.save()

    def increment_times_completed(self):
        self.times_completed = self.times_completed + 1
        self.save()

    def set_last_requested(self):
        self.last_requested = timezone.now()        
        self.save()

    def has_request_pending(self):
        if self.times_completed < self.times_requested:
            return True
        return False

    def get_completion(self):
        fields = 10.0
        completed = 3.0
        if self.participant_type != '':
            completed += 1.0
        if self.gender != '':
            completed += 1.0
        if self.graduation_year != '':
            completed += 1.0
        if self.school != '':
            completed += 1.0
        if self.industry != '':
            completed += 1.0
        if self.company != '':
            completed += 1.0
        if self.current_state != '':
            completed += 1.0
        return completed / fields * 100

    class Meta:
        ordering = ['lastname', 'firstname']


class MemberList(models.Model):
  
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization)
    members = models.ManyToManyField(Member)
    slug = models.SlugField(unique=True)
    uuid = models.CharField(max_length=100, unique=True, default=uuid.uuid1)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/memberlists/' + self.slug
  
    def get_update_url(self):
        return self.get_absolute_url() + '/update'

    def get_send_mail_url(self):
        return self.get_absolute_url() + '/send-mail'

    def get_members(self):
        return self.members.all()

    def get_email_list(self):
        email_list = '' 
        for member in self.members.all():
            email_list += member.email + ', '
        return email_list

    class Meta:
        ordering = ['name']


class AccessToken(models.Model):
    """ A one time token that allows unauthenticated users to gain access to 
        the site to edit their personal information. """
    
    token = models.CharField(max_length=255, unique=True, default=uuid.uuid1)
    used = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return str(self.token)


class AuthenticationToken(AccessToken):
    """ An AccessToken that is tied to a specific User """
  
    user = models.ForeignKey(User)
