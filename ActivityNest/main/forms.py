from django import forms
from .models import Item
from .models import category_items, year_choice


class ListForm(forms.ModelForm):
    sUsername = forms.CharField(widget=forms.TextInput(attrs={ 'class' : 'text-black ring-black ring-1 rounded-lg h-5'}))
    name = forms.CharField(widget=forms.TextInput(attrs={ 'class' : 'text-black ring-black ring-1 rounded-lg h-5'}))
    department = forms.CharField(widget=forms.TextInput(attrs={'readonly' : 'readonly', 'class' : 'text-black '}))
    category = forms.ChoiceField(choices=category_items, widget=forms.Select(attrs={'class' : 'text-black'}))
    year = forms.ChoiceField(choices=year_choice, widget=forms.Select(attrs={'class' : 'text-black'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class' : 'text-black ring-black ring-1 rounded-lg h-5'}))
    # files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))



    class Meta:
        model = Item
        fields = ("sUsername", "name", "category", "description", "department", "year")
        widgets = {
            'category' : forms.Select,
            'year' : forms.Select,
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)
        if user:
            self.fields['department'].initial = user.member.department

class UpdateListForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'class' : 'text-black ring-black ring-1 rounded-lg h-5'}))

    class Meta:
        model = Item
        fields = ["description"]
 
    def __init__(self, *args, **kwargs):
        item = kwargs.pop('item', None) 
        super().__init__(*args, **kwargs)
        if item:
            self.fields['sUsername'].initial = item.sUsername
