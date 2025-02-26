from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'password']

class LoginForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['email', 'password']