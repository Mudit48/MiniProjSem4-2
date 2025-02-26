from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # Use Django's built-in login
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Redirects to login after logout
]