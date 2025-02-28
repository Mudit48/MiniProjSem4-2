from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ListForm
from .models import Item

@login_required(login_url="/auth/login/")  # Redirects to login if not authenticated
def home(req):
    all_items = Item.objects.all()
    return render(req, 'index.html', {'all_items': all_items})


dep = ['it', 'cse', 'cs', 'extc']
def department(req, dept):

    if dept in dep:
        return render(req, 'department.html' , { "dept" : dept})
    else:
        return render(req, '404.html')

def list_item(req):
    form = ListForm()
    if req.method == 'POST':
        form = ListForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return HttpResponse("Invalid form")
    

    else:   
        return render(req, 'list_item.html', {'form' : form})