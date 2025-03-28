from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('department/<str:dept>/', views.department, name="dept"),
    path('list', views.list_item, name='list_item'),
    path("pie-chart/", views.pie_chart, name="pie_chart"),
    path("pie-chart-year/<str:dept>/", views.pie_chart_year, name="pie_chart_year_dept"),
    path("user/<str:username>/", views.profile, name="profile"),
    path("category/<str:dept>/<str:category>/", views.category_item, name="display_category"),
    path("update/<int:item_id>/", views.update, name="update"),
    path("category/<str:category>", views.category, name="category"),
    path("delete/<str:id>", views.deleteButton, name="delete"),
    path("profile/<str:username>/attend", views.prof_attend, name="prof_attend"),
    path("attend/", views.attend_view, name="attend"),
    path("__reload__/", include("django_browser_reload.urls")),

]
