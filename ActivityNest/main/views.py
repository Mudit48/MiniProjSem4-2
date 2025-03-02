from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ListForm
from .models import Item
from django.shortcuts import render, redirect
from users.models import Member 
from django.shortcuts import render
from django.http import HttpResponse
from .charts import generate_pie_chart
from .chartyear import generate_pie_chart_year
def pie_chart(request):
    buffer = generate_pie_chart()
    
    # If buffer is None, return a message instead of an image
    if buffer is None:
        return HttpResponse("No data available to generate the chart.", content_type="text/plain")

    return HttpResponse(buffer.getvalue(), content_type="image/png")

def pie_chart_year(request, dept):
    buffer = generate_pie_chart_year(dept)
    
    # If buffer is None, return a message instead of an image
    if buffer is None:
        return HttpResponse("No data available to generate the chart.", content_type="text/plain")

    return HttpResponse(buffer.getvalue(), content_type="image/png")


def home(req):
    all_items = Item.objects.all()
    return render(req, 'index.html', {'all_items': all_items ,'chart_url': '/pie-chart/'} )

dep = ['it', 'cse', 'cs', 'extc']

def department(req, dept):
    if dept in dep:
        dept_items = Item.objects.filter(department=dept)
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
    
