from django.db import models
from django.contrib.auth.models import User
# Create your models here.

dept_choice = {
    "EXTC" : "EXTC",
    "IT" : "IT",
    "CSE" : "CSE",
    "CS" : "CS"
}

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    department = models.CharField(max_length=10, default="EXTC", choices=dept_choice)

    def __str__(self):
        return self.user.email
    

    
