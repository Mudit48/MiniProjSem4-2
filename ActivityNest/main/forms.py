from django import forms
from .models import Item


class ListForm(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = ("name", "category", "description")
        widgets = {
            'category' : forms.Select,
        }
