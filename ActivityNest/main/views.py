from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ListForm, UpdateListForm, AttendForm
from .models import Item
from users.models import Member 
from .charts import generate_pie_chart
from .chartyear import generate_pie_chart_year
import cloudinary.uploader
import gspread
from google.oauth2.service_account import Credentials
from django.conf import settings
from django.contrib import messages
import google.generativeai as genai
import httpx
import base64
import ast
from django.contrib.auth.models import User



scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

creds = Credentials.from_service_account_file("credentials.json", scopes = scopes)
client = gspread.authorize(creds)

sheet_id = "1p978CHlDRzW3NiVIZYKPMjj8vfTh55AeEgqAf6lFHl0"

workbook = client.open_by_key(sheet_id)

sheet = workbook.worksheet("Sheet1")
math = workbook.worksheet("math")

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

def update(request, item_id):
    item = get_object_or_404(Item, id=item_id)  # Fetch the item

    if request.method == "POST":
        form = UpdateListForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            # Delete old files from Cloudinary
            if item.files:
                for file_url in item.files:
                    public_id = file_url.split("/")[-1].split(".")[0]  # Extract public_id
                    cloudinary.uploader.destroy(public_id)  # Delete from Cloudinary

            # Clear old files from database
            item.files.clear()

            # Upload new files
            new_files = request.FILES.getlist("files")  # Get new files
            uploaded_file_urls = []  # Store new file URLs

            allowed_extensions = ["jpg", "jpeg", "png", "gif", "webp"]
            max_file_size = 2 * 1024 * 1024  # 2MB

            for file in new_files:
                if not file.content_type.startswith("image"):  # Check if it's an image
                    messages.error(request, "Only image files are allowed!")
                    return redirect('update', item_id=item.id)

                if file.size > max_file_size:  # Check file size
                    messages.error(request, "Each file must be less than 2MB!")
                    return redirect('update', item_id=item.id)

                file_extension = file.name.split('.')[-1].lower()
                if file_extension not in allowed_extensions:  # Check file extension
                    messages.error(request, "Invalid file type! Allowed: JPG, PNG, GIF, WEBP.")
                    return redirect('update', item_id=item.id)

                upload_result = cloudinary.uploader.upload(file, resource_type="image")  # Upload to Cloudinary
                uploaded_file_urls.append(upload_result["secure_url"])  # Append new URLs

            # Update the item fields manually
            item.files = uploaded_file_urls
            item.category = form.cleaned_data["category"]
            item.description = form.cleaned_data["description"]
            item.year = form.cleaned_data["year"]
            item.doe = str(form.cleaned_data["doe"])
            item.name = form.cleaned_data["name"]

            item.save()  

            messages.success(request, "Item successfully updated!")
            return redirect("home")  
        else:
            print(form.errors)  

    else:
        form = UpdateListForm(instance=item)

    return render(request, "update_item.html", {"form": form})

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
            return render(req, 'department.html' , { "dept" : dept, 'all_items' :dept_items, 'chart_year_url': '/pie-chart-year/', 'member' : member, 'word' : word } )
        else:
            return render(req, 'department.html' , { "dept" : dept, 'all_items' :dept_items, 'chart_year_url': '/pie-chart-year/', 'word' : word} )
    else:
        return render(req, '404.html')
    
def profile(request, username):


    user_items = Item.objects.filter(sUsername__iexact=username)

    
    try:
        userR = get_object_or_404(User, username=username)
        user_mem = get_object_or_404(Member, user=userR)
    except:
        userR=None

    curr_member = get_object_or_404(Member, user=request.user)
    if request.user.is_authenticated and userR != None:
        

        return render(request, 'profile.html', {
        'all_items': user_items,
        'member': curr_member,
        'username': username,
        'user': request.user,
        'prof_user' : userR,
        'profile' : user_mem,
        
    })

    else:
        return render(request, 'profile.html', {
        'all_items': user_items,
        'member': curr_member,
        'username': username,
        'user': request.user,
        'prof_user' : userR,
        
    })



    
def category_item(req, dept, category):
    category_items = Item.objects.filter(category__iexact=category, department__iexact=dept)
    if req.user.is_authenticated:
        member = get_object_or_404(Member, user=req.user)
        print(member.roles)
        return render(req, 'category_dept.html', {'all_items': category_items, 'dept' : dept, 'member' : member, 'category' : category})
    else:
        return render(req, 'category_dept.html', {'all_items': category_items, 'dept' : dept, 'category' : category})
    
    

def category(req, category):
    category_items = Item.objects.filter(category__iexact=category)
    if req.user.is_authenticated:
        member = get_object_or_404(Member, user=req.user)
        print(member.roles)
        return render(req, 'category.html', {'all_items': category_items, 'member' : member, 'category' : category})
    else:
        return render(req, 'category.html', {'all_items': category_items, 'category' : category})
    
    
    

@login_required
def list_item(req):
    form = ListForm()
    department = req.user.member.department
    teacher = req.user.member.full_name
    print(teacher)
    

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
            uploaded_urls = []  # Store uploaded file URLs

            allowed_extensions = ["jpg", "jpeg", "png", "gif", "webp"]
            max_file_size = 2 * 1024 * 1024  # 2MB

            for file in files:
                if not file.content_type.startswith("image"):  # Check if it's an image
                    messages.error(req, "Only image files are allowed!")
                    return redirect('list_item')

                if file.size > max_file_size:  # Check file size
                    messages.error(req, "Each file must be less than 2MB!")
                    return redirect('list_item')

                file_extension = file.name.split('.')[-1].lower()
                if file_extension not in allowed_extensions:  # Check file extension
                    messages.error(req, "Invalid file type! Allowed: JPG, PNG, GIF, WEBP.")
                    return redirect('list_item')

                upload_result = cloudinary.uploader.upload(file, resource_type="image")  # Upload to Cloudinary
                uploaded_urls.append(upload_result["secure_url"])  # Store URL

            item.files = uploaded_urls
            item.department = department
            item.teacher = teacher
            item.save()
            item.refresh_from_db()
            id = item.id
            sheet.append_row([id, name, username, department, category, description, year, doe])
            
            messages.success(req, "Item successfully added!")
            return redirect('home')

        else:
            messages.error(req, "Invalid form submission!")
            return redirect('list_item')

    else:   
        form = ListForm(user=req.user)
        return render(req, 'list_item.html', {'form': form, 'department': department})
    
from datetime import datetime
from collections import defaultdict

def attend_view(req):
    genai.configure(api_key="AIzaSyBi-lF7PEra0qfk-1CKxaLnoEEZGqICY1k")
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")

    form = AttendForm()

    if req.method == "POST":
        form = AttendForm(req.POST, req.FILES)

        roll_image = req.FILES.get('attend_file')
        roll_date = req.POST.get('roll_date')
        time_slot = req.POST.get('time_slot') 

        if roll_image:
            upload_result = cloudinary.uploader.upload(roll_image)
            roll_image_url = upload_result.get('secure_url')

            image = httpx.get(roll_image_url)

            prompt = (
                "Extract all the roll numbers visible in the image. "\
                    "Return only a Python list of integers representing the extracted roll numbers."\
                   "Do not add any extra text, explanations, or formatting."\
                    "ONLY return the list in this format: [16, 31, 29, 51]."
            )
            response = model.generate_content([{'mime_type':'image/jpeg', 'data': base64.b64encode(image.content).decode('utf-8')}, prompt])
            cap = str(response.text)
            print(cap)
            print(len(cap))

            try:
                extracted_numbers = ast.literal_eval(cap)  
                if not isinstance(extracted_numbers, list):
                    raise ValueError("Invalid AI response format")
                
                extracted_numbers = [num for num in extracted_numbers if isinstance(num, int) and 1 <= num <= 70]
                
                actual_list = ['P'] * 70  
                for num in extracted_numbers:
                    actual_list[num - 1] = 'A' 

            except (SyntaxError, ValueError) as e:
                print("Error parsing response:", e)
                return render(req, 'attend.html', {'form': form, 'error': 'Error processing image data'})


            formatted_time = datetime.strptime(time_slot, "%H:%M").strftime("%I:%M %p")

            data = math.get_all_values()

            date_column = None
            

            date_column = len(data[0]) + 1
            math.update_cell(1, date_column, roll_date)
            

            existing_col_data = math.col_values(date_column)
            next_available_row = len(existing_col_data) + 1 if len(existing_col_data) > 1 else 2  # Start from row 2

            final_list = actual_list

            if next_available_row == 2:
                math.update_cell(2, date_column, formatted_time) 

            attendance_range = f"{gspread.utils.rowcol_to_a1(3, date_column)}:{gspread.utils.rowcol_to_a1(72, date_column)}"
            math.update(attendance_range, [[val] for val in final_list])  

        return render(req, 'index.html', {'form': form})

    return render(req, 'attend.html', {'form': form})