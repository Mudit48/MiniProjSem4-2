from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ListForm, UpdateListForm
from .models import Item
from users.models import Member 
from .charts import generate_pie_chart
from .chartyear import generate_pie_chart_year
import cloudinary.uploader
import gspread
from google.oauth2.service_account import Credentials
from django.conf import settings
from django.contrib.auth.models import User

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

creds = Credentials.from_service_account_file("credentials.json", scopes = scopes)
client = gspread.authorize(creds)

sheet_id = "1p978CHlDRzW3NiVIZYKPMjj8vfTh55AeEgqAf6lFHl0"

workbook = client.open_by_key(sheet_id)

sheet = workbook.worksheet("Sheet1")

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
    all_items = Item.objects.all().order_by('-id')
    form = UpdateListForm()
    username = req.user.username
    user = req.user
    word = "home"
    
    if req.user.is_authenticated:
        member = get_object_or_404(Member, user=req.user)
      
        print(member.roles)
        return render(req, 'index.html', {'all_items': all_items ,'chart_url': '/pie-chart/', 'curr_username' : username,  'form' : form , 'user' : user , 'member' : member, 'word' : word } )
    else:
        return render(req, 'index.html', {'all_items': all_items ,'chart_url': '/pie-chart/', 'curr_username' : username,  'form' : form , 'user' : user, 'word' : word } )

def updt(request, item_id):
    item = get_object_or_404(Item, id=item_id)  

    if request.method == "POST":
        form = UpdateListForm(request.POST, instance=item)  
        if form.is_valid():
            print(form)
            form.save()  
            return redirect('home') 
        else:
            print(form.errors)
    
    else:
        form = UpdateListForm(instance=item)  

    return redirect('home')

def deleteButton(req, id):
    cell = sheet.find(str(id), in_column=1)
    sheet.delete_rows(cell.row)
    item = Item.objects.get(id=id)
    item.delete()
    return redirect('home')



dep = ['it', 'cse', 'cs', 'extc']

def department(req, dept):
    if dept in dep:
        dept.upper()
        word = "home"
        dept_items = Item.objects.filter(department__iexact=dept)
        if req.user.is_authenticated:
            member = get_object_or_404(Member, user=req.user)
            return render(req, 'department.html' , { "dept" : dept, 'dept_items' :dept_items, 'chart_year_url': '/pie-chart-year/', 'member' : member, 'word' : word } )
        else:
            return render(req, 'department.html' , { "dept" : dept, 'dept_items' :dept_items, 'chart_year_url': '/pie-chart-year/', 'word' : word} )
    else:
        return render(req, '404.html')
    
def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_mem = get_object_or_404(Member, user=user)
    user_items = Item.objects.filter(sUsername__iexact=username)

    return render(request, 'profile.html', {
        'user_items': user_items,
        'member': user_mem,
        'username': username,
        'user': user_mem,
    })

def category_item(req, dept, category):
    category_items = Item.objects.filter(category__iexact=category, department__iexact=dept)
    if req.user.is_authenticated:
        member = get_object_or_404(Member, user=req.user)
        print(member.roles)
        return render(req, 'category_dept.html', {'category_items': category_items, 'dept' : dept, 'member' : member, 'category' : category})
    else:
        return render(req, 'category_dept.html', {'category_items': category_items, 'dept' : dept, 'category' : category})
    
    

def category(req, category):
    category_items = Item.objects.filter(category__iexact=category)
    if req.user.is_authenticated:
        member = get_object_or_404(Member, user=req.user)
        print(member.roles)
        return render(req, 'category.html', {'category_items': category_items, 'member' : member, 'category' : category})
    else:
        return render(req, 'category.html', {'category_items': category_items, 'category' : category})
    
    
    

@login_required
def list_item(req):
    form = ListForm()
    department = req.user.member.department
    
    if req.method == 'POST':
        form = ListForm(req.POST, req.FILES, user=req.user)
        if form.is_valid():
            
            name = form.cleaned_data["name"]
            username = form.cleaned_data["sUsername"]
            category = form.cleaned_data["category"]
            description = form.cleaned_data["description"]
            year = form.cleaned_data["year"]
            doe = str(form.cleaned_data["doe"])

            item = form.save(commit=False)
            files = req.FILES.getlist("files")  # Get multiple files from form
            print(len(files))
            uploaded_urls = []  # Store uploaded file URLs

            for file in files:
                upload_result = cloudinary.uploader.upload(file,resource_type="auto")  # Upload to Cloudinary
                uploaded_urls.append(upload_result["secure_url"])  # Store URL

            item.files=uploaded_urls
            item.department = department
            item.save()
            item.refresh_from_db()
            id = item.id
            sheet.append_row([id,name,username,department,category,description,year,doe])
            return redirect('home')
        else:
            return HttpResponse("Invalid form")
    

    else:   
        form = ListForm(user=req.user)
        return render(req, 'list_item.html', {'form' : form, 'department' : department})
    
