from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('department/<str:dept>/', views.department, name="dept"),

    path('list', views.list_item, name='list_item'),
]
