from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template

from alumnus_backend.models import Organization, Member, MemberList, AuthenticationToken


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
            context = {'user': user, 'token': token}
            context = Context(context)
            text_content = get_template('emails/user_activate_email.txt').render(context)
            html_content = get_template('emails/user_activate_email.html').render(context)
            to = user.email
            subject, from_email = 'Activate your Alumnus acount', settings.DEFAULT_FROM_EMAIL
            msg = EmailMultiAlternatives('Activate your Alumnus account', text_content, from_email, [to])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
        return user


class OrganizationForm(forms.ModelForm):
    
    class Meta:
        model = Organization 
        exclude = ('owner', 'uuid',)


class MemberForm(forms.ModelForm):
    
    class Meta:
        model = Member
        exclude = ('organization', 'uuid',)


class MemberListForm(forms.ModelForm):

    class Meta:
        model = MemberList
        exclude = ('organization', 'uuid',)
        widgets = {
          'members': forms.CheckboxSelectMultiple()
        }

    def __init__(self, organization, *args, **kwargs):
        super(MemberListForm, self).__init__(*args, **kwargs)
        self.fields['members'] = forms.ModelMultipleChoiceField(
            queryset=Member.objects.filter(organization=organization),
            widget=forms.CheckboxSelectMultiple(),
        )


class MemberImportForm(forms.Form):

    file = forms.FileField(label='Import Excel file')

    def clean(self):
        data = super(MemberImportForm, self).clean()

        # Double check that the file is there
        if 'file' not in data:
            raise forms.ValidationError('Please submit an Excel file.', code='invalid')

        # Ensure that the submitted file has an Excel extension
        docfile = data['file']
        extension = docfile.name.split('.')[1]
        if extension != 'xlsx':
            raise forms.ValidationError('%s is not a valid Excel file. Please make sure your input file is an Excel file.' % docfile.name, code='invalid') 

        return data

