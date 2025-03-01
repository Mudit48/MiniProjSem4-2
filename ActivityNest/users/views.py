from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import Member
from .forms import MemberForm, LoginForm

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from .models import Member
from .forms import MemberForm

def register(req):
    if req.method == "POST":
        form = MemberForm(req.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            department = form.cleaned_data['department']

            if User.objects.filter(username=email).exists():
                messages.error(req, "This email is already registered. Try logging in.")
                return render(req, 'register.html', {'form': form})

            user = User.objects.create_user(username=email, email=email, password=password)

            member = Member.objects.create(user=user, department=department)

            messages.success(req, 'Registration successful! You can now log in.')
            return redirect('login')

    form = MemberForm()
    return render(req, 'register.html', {'form': form})


def login_user(req):
    if req.method == "POST":
        form = LoginForm(req.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Fetch user using email (since authenticate expects username)
            user = User.objects.filter(email=email).first()
            if user:
                user = authenticate(username=user.username, password=password)

            if user is not None:
                login(req, user)
                return redirect('home')
            else:
                return render(req, 'login.html', {'form': form, 'message': 'Invalid email or password'})
    
    return render(req, 'login.html')

def logout_user(req):
    logout(req)
    return redirect('login')
