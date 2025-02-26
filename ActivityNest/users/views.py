from django.shortcuts import render
from .models import Member
from .forms import MemberForm, LoginForm

# Create your views here.
def register(req):
    if req.method == "POST":
        form = MemberForm(req.POST or None)
        if form.is_valid():
            form.save()
            return render(req, 'register.html')
    else:
        return render(req, 'register.html')
    

def login(req):
    if req.method == "POST":
        form = LoginForm(req.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            members = Member.objects.filter(email=email, password=password)
            if members:
                return render(req, 'index.html')
            else:
                return render(req, 'login.html', {"error": "Invalid email or password"})
            
            # Now you can use the email variable
            
        else:
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(email,password)
    else:
        return render(req, 'login.html')