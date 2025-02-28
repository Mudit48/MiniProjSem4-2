from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),  # Use Django's built-in login
    path('logout/', views.logout_user, name='logout'),  # Redirects to login after logout
]