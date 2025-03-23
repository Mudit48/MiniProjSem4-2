from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import Member
from .forms import MemberForm, LoginForm
import cloudinary.uploader

def register(req):
    if req.method == "POST":
        form = MemberForm(req.POST,req.FILES)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            department = form.cleaned_data['department']
            profile_picture = req.FILES.get('profile_picture')

            if User.objects.filter(username=username).exists():
                messages.error(req, "This username is already taken.")
                return render(req, 'register.html', {'form': form})

            user = User.objects.create_user( username=username, email=email, password=password)
            # Upload profile picture to Cloudinary (if provided)
            profile_picture_url = None
            if profile_picture:
                upload_result = cloudinary.uploader.upload(profile_picture)
                profile_picture_url = upload_result.get('secure_url')

            member = Member.objects.create(user=user, full_name = full_name,department=department, profile_picture=profile_picture_url)

            messages.success(req, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            return render(req, 'register.html', {'form': form})

    form = MemberForm()
    return render(req, 'register.html', {'form': form})


def login_user(req):
    if req.method == "POST":
        form = LoginForm(req.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.filter(email=email).first()
            if user:
                user = authenticate(username=user.username, password=password)

            if user is not None:
                login(req, user)
                return redirect('home')
            else:
                return render(req, 'login.html', {'form': form, 'message': 'Invalid email or password'})
        else:
            return render(req, 'login.html', {'form': form, 'message': 'Invalid email or password'})
    else:
        return render(req, 'login.html')

def logout_user(req):
    logout(req)
    return redirect('home')
