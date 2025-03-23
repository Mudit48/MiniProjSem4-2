from django.db import models
from django.utils import timezone

# Create your models here.

category_items = {
    'achievement' : "achievement",
    'placement' : "placement",
    'certificate' : "certificate",
}

year_choice = {
    "SE" : "SE",
    "TE" : "TE",
    "BE" : "BE",
}


class Item(models.Model):
    sUsername = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=False, choices=category_items)
    description = models.CharField(max_length=200)
    date_posted = models.DateField(auto_now_add=True)
    department = models.CharField(max_length=4)
    year = models.CharField(max_length=2, null=True, choices=year_choice)
    files=models.JSONField(default=list)
    doe= models.DateField(null=True)
    teacher=models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name

class Attend(models.Model):
    roll_no = models.IntegerField(max_length=2, null=False)
    name = models.CharField(max_length=100,default=0, null=False)
    math = models.CharField(max_length=3,default=0, null=True)
    at = models.CharField(max_length=3,default=0, null=True)
    cn = models.CharField(max_length=3,default=0, null=True)
    coa = models.CharField(max_length=3,default=0, null=True)
    os = models.CharField(max_length=3,default=0, null=True)
    python = models.CharField(max_length=3,default=0, null=True)


    roll_image = models.URLField(null=True)
    roll_date = models.DateField(null=True)