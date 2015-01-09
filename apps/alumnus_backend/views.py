from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Organization, Member


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username, email, password)
        user.save()
        return HttpResponse(user)
    else:
        return HttpResponse('This endpoint does not support GET requests')

@login_required
def get_organizations(request):
    if request.method == 'GET':
        organizations = Organization.objects.filter(owner=request.user)
        return HttpResponse(organizations)
