from django import forms
from .models import Item
from .models import category_items, year_choice

class ListForm(forms.ModelForm):
    sUsername = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:outline-none text-lg'
        })
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:outline-none text-lg'
        })
    )
    department = forms.CharField(
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
            'class': 'w-full p-3 bg-gray-200 border border-gray-300 rounded-lg focus:outline-none text-lg'
        })
    )
    category = forms.ChoiceField(
        choices=category_items,
        widget=forms.Select(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:outline-none text-lg'
        })
    )
    year = forms.ChoiceField(
        choices=year_choice,
        widget=forms.Select(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:outline-none text-lg'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:outline-none text-lg resize-none',
            'rows' : '2'
        })
    )
    # files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Item
        fields = ("sUsername", "name", "category", "description", "department", "year")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)
        if user:
            self.fields['department'].initial = user.member.department

class UpdateListForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:outline-none text-lg resize-none'
        })
    )

    class Meta:
        model = Item
        fields = ["description"]

    def __init__(self, *args, **kwargs):
        item = kwargs.pop('item', None) 
        super().__init__(*args, **kwargs)
        if item:
            self.fields['sUsername'].initial = item.sUsername
