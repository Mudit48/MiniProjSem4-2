from django.db import models
from django.contrib.auth.models import User
# Create your models here.

dept_choice = {
    "EXTC" : "EXTC",
    "IT" : "IT",
    "CSE" : "CSE",
    "CS" : "CS"
}

year_choice = {
    "SE" : "SE",
    "TE" : "TE",
    "BE" : "BE",
}

class RoleChoices(models.TextChoices):
    TEACHER = "Teacher", "Teacher"
    STUDENT = "Student", "Student"

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)    
    department = models.CharField(max_length=10, default="EXTC", choices=dept_choice)
    year = models.CharField(max_length=10, null=True, default="SE", choices=year_choice)
    roles = models.CharField(max_length=20 , default=RoleChoices.STUDENT,choices=RoleChoices.choices)
    profile_picture = models.URLField(max_length=500, blank=True, null=True)  # Cloudinary image URL


    def __str__(self):
        return self.user.email
    


