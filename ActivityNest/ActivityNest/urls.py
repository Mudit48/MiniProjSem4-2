from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from . import views

def redirect_to_login(request):
    return redirect("login")  # Redirects unauthenticated users to login page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),  # Home page (will enforce login in views)
    path('auth/', include("users.urls")),  # Authentication URLs
    path("__reload__/", include("django_browser_reload.urls")),
]
