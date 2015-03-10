import itertools

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from django.utils.text import slugify

from alumnus_backend.models import Organization, Member, MemberList, AuthenticationToken
from .parser import ExcelParser


class CustomUserCreationForm(UserCreationForm):
    
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.is_active = False
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create a new AuthenticationToken
            token = AuthenticationToken()
            token.user = user
            token.save()
            # Let the user know about it
            context = {
                'user': user, 
                'token': token,
                'site_name': settings.SITE_NAME
            }
            context = Context(context)
            text_content = get_template('emails/user_activate_email.txt').render(context)
            html_content = get_template('emails/user_activate_email.html').render(context)
            to = user.email
            subject, from_email = 'Activate your Alumnus acount', settings.DEFAULT_FROM_EMAIL
            msg = EmailMultiAlternatives('Activate your Alumnus account', text_content, from_email, [to])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
        return user


class UserUpdateEmailForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email']
    
    email = forms.EmailField(required=True)


class UserUpdatePasswordForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = []
    
    password1 = forms.CharField(label=("Password"), widget=forms.PasswordInput) 
    password2 = forms.CharField(label=("Password confirm"), widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.", code='invalid')
        return password2


class OrganizationForm(forms.ModelForm):

    name = forms.CharField(label=("Organization Name"))
    
    class Meta:
        model = Organization 
        exclude = ('owner', 'privileged_users', 'slug', 'uuid',)

    def save(self, owner, commit=True):
        instance = super(OrganizationForm, self).save(commit=False)

        # set owner
        instance.owner = owner

        # set slug if not already set
        if not instance.slug:
            max_length = Organization._meta.get_field('slug').max_length
            instance.slug = orig = slugify(instance.name)[:max_length]
            for x in itertools.count(1):
                if not Organization.objects.filter(slug=instance.slug).exists():
                    break
                # Truncate the original slug dynamically. Minus 1 for the hyphen.
                instance.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

        if commit:
            instance.save()
        return instance
          

class MemberForm(forms.ModelForm):

    email = forms.EmailField(label='Personal Email')
    
    class Meta:
        model = Member
        exclude = ('organization', 'last_requested', 'slug', 'times_completed', 'times_requested', 'uuid',)

    def save(self, organization, commit=True):
        instance = super(MemberForm, self).save(commit=False)

        # set organization
        instance.organization = organization

        # set slug if not already set
        if not instance.slug:
            max_length = Member._meta.get_field('slug').max_length
            instance.slug = orig = slugify(instance.__unicode__())[:max_length]
            for x in itertools.count(1):
                if not Member.objects.filter(slug=instance.slug).exists():
                    break
                # Truncate the original slug dynamically. Minus 1 for the hyphen.
                instance.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

        # save
        if commit:
            instance.save()
        return instance


class MemberListForm(forms.ModelForm):

    class Meta:
        model = MemberList
        exclude = ('organization', 'slug', 'uuid',)
        widgets = {
          'members': forms.CheckboxSelectMultiple()
        }

    def __init__(self, organization, *args, **kwargs):
        super(MemberListForm, self).__init__(*args, **kwargs)
        self.fields['members'] = forms.ModelMultipleChoiceField(
            queryset=Member.objects.filter(organization=organization),
            widget=forms.CheckboxSelectMultiple(),
        )

    def save(self, organization, commit=True):
        instance = super(MemberListForm, self).save(commit=False)

        # set organization
        instance.organization = organization

        # set slug if not already set
        if not instance.slug:
            max_length = MemberList._meta.get_field('slug').max_length
            instance.slug = orig = slugify(instance.name)[:max_length]
            for x in itertools.count(1):
                if not MemberList.objects.filter(slug=instance.slug).exists():
                    break
                # Truncate the original slug dynamically. Minus 1 for the hyphen.
                instance.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

        if commit: 
            instance.save()
        return instance
        

class MemberImportForm(forms.Form):

    file = forms.FileField(label='Excel or CSV File')

    def clean(self):
        data = super(MemberImportForm, self).clean()

        # Double check that the file is there
        if 'file' not in data:
            raise forms.ValidationError('Please submit an Excel file.', code='invalid')

        # Ensure that the submitted file has an Excel extension
        docfile = data['file']
        extensions = ['xlsx']
        extension = docfile.name.split('.')[1]
        if extension not in extensions:
            raise forms.ValidationError('%s is not a valid Excel file. Please make sure your input file is an Excel file.' % docfile.name, code='invalid') 

        # Check that the format of the uploaded file is expected
        self.parser = ExcelParser(docfile)
        if not self.parser.validate():
            raise forms.ValidationError('%s does not match the format of the template Excel file provided.' % docfile.name, code='invalid')
    
        return data

    def save(self, organization):
        self.parser.parse(organization)
        

