from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ListForm, UpdateListForm
from .models import Item
from users.models import Member 
from .charts import generate_pie_chart
from .chartyear import generate_pie_chart_year

def pie_chart(request):
    buffer = generate_pie_chart()
    
    # If buffer is None, return a message instead of an image
    if buffer is None:
        return HttpResponse("No data available to generate the chart.", content_type="text/plain")

    return HttpResponse(buffer.getvalue(), content_type="image/png")

def pie_chart_year(request, dept):
    buffer = generate_pie_chart_year(dept.upper())
    
    if buffer is None:
        return HttpResponse("No data available to generate the chart.", content_type="text/plain")

    return HttpResponse(buffer.getvalue(), content_type="image/png")


def home(req):
    all_items = Item.objects.all()
    form = UpdateListForm()
    username = req.user.username
    return render(req, 'index.html', {'all_items': all_items ,'chart_url': '/pie-chart/', 'curr_username' : username,  'form' : form} )

def updt(request, item_id):
    item = get_object_or_404(Item, id=item_id)  # Fetch the existing item

    if request.method == "POST":
        form = UpdateListForm(request.POST, instance=item)  # Ensure using UpdateListForm
        if form.is_valid():
            print(form)
            form.save()  # Update only the description
            return redirect('home')  # Redirect to the homepage
        else:
            print(form.errors)
    
    else:
        form = UpdateListForm(instance=item)  # Load existing data

    return redirect('home')



dep = ['it', 'cse', 'cs', 'extc']

def department(req, dept):
    if dept in dep:
        dept.upper()
        dept_items = Item.objects.filter(department__iexact=dept)
        return render(req, 'department.html' , { "dept" : dept, 'dept_items' :dept_items, 'chart_year_url': '/pie-chart-year/'} )
    else:
        return render(req, '404.html')
    

@login_required
def list_item(req):
    form = ListForm()
    department = req.user.member.department
    if req.method == 'POST':
        form = ListForm(req.POST, user=req.user)
        if form.is_valid():
            item = form.save(commit=False)
            item.department = department
            form.save()
            return redirect('home')
        else:
            return HttpResponse("Invalid form")
    

    else:   
        form = ListForm(user=req.user)
        return render(req, 'list_item.html', {'form' : form, 'department' : department})
    
