import uuid
from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/organizations/' + str(self.pk)
  
    def get_members_url(self):
        return self.get_absolute_url() + '/members'

    def get_create_member_url(self):
        return self.get_members_url() + '/create'

    def get_memberlists_url(self):
        return self.get_absolute_url() + '/memberlists'
  
    def get_create_memberlist_url(self):
        return self.get_memberlists_url() + '/create'


class Member(models.Model):
    
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization)
    uuid = models.CharField(max_length=100, unique=True, default=uuid.uuid1)

    def __unicode__(self):
        return self.firstname + ' ' + self.lastname

    def get_absolute_url(self):
        return '/members/' + str(self.pk)

    def get_update_url(self):
        return self.get_absolute_url() + '/update'

    def get_update_request_url(self):
        return self.get_absolute_url() + '/update-request'

    def get_public_update_url(self):
        # Create a new AccessToken every time this function is called
        token = AccessToken()
        token.save()
        return self.get_update_url() + '/' + str(token)


class MemberList(models.Model):
  
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization)
    members = models.ManyToManyField(Member)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/memberlists/' + str(self.pk)
  
    def get_update_url(self):
        return self.get_absolute_url() + '/update'


class AccessToken(models.Model):
    
    token = models.CharField(max_length=255, unique=True, default=uuid.uuid1)
    used = models.BooleanField(default=False)
    
    def __unicode__(self):
        return str(self.token)
