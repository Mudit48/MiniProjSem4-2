from django.shortcuts import render,redirect
from .models import Member
from .forms import MemberForm, LoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def register(req):
    if req.method == "POST":
        form = MemberForm(req.POST or None)
        if form.is_valid():
            email = req.POST['email']
            password = req.POST['password']

            user = User.objects.create_user(
                username = req.POST['email'],
                email = email,
                password =password
            )
            user.save()
            form.save()
            messages.success(req, 'Registration was successful!')
            return redirect('login')
        else:
            return render(req, 'register.html', {'form': form, 'message': 'Invalid form data'})
    else:
        form = MemberForm()
        return render(req, 'register.html', {'form': form})
    
def login_user(req):
    if req.method == "POST":
        form = LoginForm(req.POST or None)
        if form.is_valid():
            email = req.POST['email']
            password = req.POST['password']
            print(email,password)
            user = authenticate(username=email, password=password)
            print(user)
            if user is not None:
                login(req, user)
                return redirect('home')
            else:
                return render(req, 'login.html', {'form': form, 'message': 'Invalid username or password'})
    else:
        return render(req, 'login.html')
    
def logout_user(req):
    logout(req)
    return redirect('login')
                                                  

