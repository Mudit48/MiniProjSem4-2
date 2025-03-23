from django import forms
from .models import Item, Attend
from .models import category_items, year_choice
from users.models import Member

class ListForm(forms.ModelForm):
    doe = forms.DateField(
        label = 'Date of event',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:outline-none text-lg'
        })
    )
    
    sUsername = forms.CharField(
        label = 'Username of student',
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:outline-none text-lg'
        })
    )
    name = forms.CharField(
        label = 'Name of student',
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:outline-none text-lg'
        })
    )
    department = forms.CharField(
        label = 'Department',
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
            'class': 'w-full p-3 bg-gray-200 border border-gray-300 rounded-lg focus:outline-none text-lg'
        })
    )
    category = forms.ChoiceField(
        label = 'Category',
        choices=category_items,
        widget=forms.Select(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:outline-none text-lg'
        })
    )
    year = forms.ChoiceField(
        label = 'Year of Study',
        choices=year_choice,
        widget=forms.Select(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:outline-none text-lg'
        })
    )
    description = forms.CharField(
        label = 'Event Description',
        widget=forms.Textarea(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:outline-none text-lg resize-none',
            'rows' : '2'
        })
    )
    # files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Item
        fields = ("sUsername", "name", "category", "description", "department", "year", "doe")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)
        if user:
            self.fields['department'].initial = user.member.department

class UpdateListForm(forms.ModelForm):
    doe = forms.DateField(
        label="Date of event",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:outline-none text-lg'
        })
    )

    name = forms.CharField(
        label="Name of student",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:outline-none text-lg'
        })
    )

    department = forms.CharField(
        label="Department",
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
            'class': 'w-full p-3 bg-gray-200 border border-gray-300 rounded-lg focus:outline-none text-lg'
        })
    )

    category = forms.ChoiceField(
        label="Category",
        choices=category_items,
        widget=forms.Select(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:outline-none text-lg'
        })
    )

    year = forms.ChoiceField(
        label="Year of Study",
        choices=year_choice,  # Replace with your choices
        widget=forms.Select(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:outline-none text-lg'
        })
    )

    description = forms.CharField(
        label="Event Description",
        widget=forms.Textarea(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:outline-none text-lg resize-none',
            'rows': '2'
        })
    )

    class Meta:
        model = Item
        fields = ["category", "description", "department", "year", "doe", "name"]

    def __init__(self, *args, **kwargs):
        item = kwargs.pop('item', None)
        super().__init__(*args, **kwargs)
        if item:
            self.fields['department'].initial = item.department  # Keep department readonly


class AttendForm(forms.ModelForm):
    class Meta:
        model = Attend
        fields = ["roll_date"]