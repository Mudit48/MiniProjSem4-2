from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from . import views

def redirect_to_login(request):
    return redirect("login")  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("main.urls")),  
    path('', include("main.urls")),  
    path('auth/', include("users.urls")),  
    path("__reload__/", include("django_browser_reload.urls")),
]
