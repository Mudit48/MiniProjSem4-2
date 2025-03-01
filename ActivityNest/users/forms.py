from django import forms
from .models import Member, dept_choice

class MemberForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full my-2 bg-[#1c1c24] text-white rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-purple-600',
        'placeholder': 'Email'
    }), label='')

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full my-2 bg-[#1c1c24] text-white rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-purple-600',
        'placeholder': 'Password'
    }), label='')

    department = forms.ChoiceField(choices=dept_choice, widget=forms.Select(attrs={
        'class': 'w-52 my-2 bg-[#1c1c24] text-white rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-purple-600'
    }), label='')

    class Meta:
        model = Member
        fields = ['department']  # Only department (email & password handled in views)


class LoginForm(forms.Form):  # Use Form instead of ModelForm
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full my-2 bg-[#1c1c24] text-white rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-purple-600',
        'placeholder': 'Email'
    }), label='')

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full my-2 bg-[#1c1c24] text-white rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-purple-600',
        'placeholder': 'Password'
    }), label='')
