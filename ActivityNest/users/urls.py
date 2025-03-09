from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),  
    path('logout/', views.logout_user, name='logout'),  
    path("__reload__/", include("django_browser_reload.urls")),

]