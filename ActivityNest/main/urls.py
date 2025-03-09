from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('department/<str:dept>/', views.department, name="dept"),
    path('list', views.list_item, name='list_item'),
    path("pie-chart/", views.pie_chart, name="pie_chart"),
    path("pie-chart-year/<str:dept>/", views.pie_chart_year, name="pie_chart_year_dept"),
    path("update/<int:item_id>/", views.updt, name="update"),
    path("__reload__/", include("django_browser_reload.urls")),

]
