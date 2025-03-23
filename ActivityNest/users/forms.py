from django import forms
from .models import Member, dept_choice, year_choice

class MemberForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-52 my-2 bg-[#1c1c24] text-white rounded-lg p-2 focus:outline-none w-full focus:ring-2 focus:ring-purple-600', 'placeholder' : 'Full Name'
    }), label='')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-52 my-2 bg-[#1c1c24] text-white rounded-lg p-2 focus:outline-none w-full focus:ring-2 focus:ring-purple-600', 'placeholder' : 'username'
    }), label='')

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full my-2 bg-[#1c1c24] text-white rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-purple-600',
        'placeholder': 'Email'
    }), label='')

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full my-2 bg-[#1c1c24] text-white rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-purple-600',
        'placeholder': 'Password'
    }), label='')

    department = forms.ChoiceField(choices=dept_choice, widget=forms.Select(attrs={
        'class': 'w-52 my-2 bg-[#1c1c24] text-white rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-purple-600 inline-block'
    }), label='')

    year = forms.ChoiceField(choices=year_choice, widget=forms.Select(attrs={
        'class': 'w-52 my-2 bg-[#1c1c24] text-white rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-purple-600 inline-block'
    }), label='')

    profile_picture = forms.ImageField(required=False)  # Accepts images

    class Meta:
        model = Member
        fields = ['full_name', 'department'] 


class LoginForm(forms.Form):  # Use Form instead of ModelForm
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full my-2 bg-[#1c1c24] text-white rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-purple-600',
        'placeholder': 'Email'
    }), label='')

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full my-2 bg-[#1c1c24] text-white rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-purple-600',
        'placeholder': 'Password'
    }), label='')
