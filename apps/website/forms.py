from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from alumnus_backend.models import Organization, Member, MemberList


class CustomUserCreationForm(UserCreationForm):
    
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class OrganizationForm(forms.ModelForm):
    
    class Meta:
        model = Organization 
        exclude = ('owner',)

class MemberForm(forms.ModelForm):
    
    class Meta:
        model = Member
        exclude = ('organization', 'uuid',)

class MemberListForm(forms.ModelForm):

    class Meta:
        model = MemberList
        exclude = ('organization',)

    def __init__(self, organization, *args, **kwargs):
        super(MemberListForm, self).__init__(*args, **kwargs)
        self.fields['members'] = forms.ModelMultipleChoiceField(
            queryset=Member.objects.filter(organization=organization),
            widget=forms.CheckboxSelectMultiple(),
        )

