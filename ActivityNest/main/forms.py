from django import forms
from .models import Item


class ListForm(forms.ModelForm):
    department = forms.CharField(widget=forms.TextInput(attrs={'readonly' : 'readonly'}))

    class Meta:
        model = Item
        fields = ("name", "category", "description", "department", "year")
        widgets = {
            'category' : forms.Select,
            'year' : forms.Select,
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)
        if user:
            self.fields['department'].initial = user.member.department
