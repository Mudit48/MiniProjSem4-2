from django.db import models
from django.utils import timezone

# Create your models here.

category_items = {
    'achv' : "achievements",
    'plcm' : "placements",
    'crtf' : "certificates",

}


class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=5, blank=False, choices=category_items)
    description = models.CharField(max_length=200)
    date_posted = models.DateTimeField(auto_now_add=True)
    #image = models.ImageField()

    def __str__(self):
        return self.name + ' ' + self.date_posted

