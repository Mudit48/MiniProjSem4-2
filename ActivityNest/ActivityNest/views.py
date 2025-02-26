from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url="/auth/login/")  # Redirects to login if not authenticated
def home(req):
    return render(req, 'index.html')

