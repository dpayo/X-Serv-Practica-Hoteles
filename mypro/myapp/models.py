from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Hotel (models.Model):
    name=models.CharField(max_length=200,default="")
    url = models.URLField(max_length=300,default="")
    body=models.TextField(max_length=800,default="")
    address= models.CharField(max_length=200,default="")
    source= models.URLField(max_length=300,default="")
    stars =models.CharField(max_length=300,default="")
    tipo=models.CharField(max_length=300,default="")

class PagUser (models.Model):
    user=models.CharField(max_length=300,default="")
    title= models.CharField(max_length=300,default="")
    color = models.CharField(max_length=300,default="")
    size=models.CharField(max_length=200,default="")
class HotelsUser(models.Model):
    user=models.CharField(max_length=300,default="")
    hotel=models.ForeignKey(Hotel)
    date = models.DateField(auto_now=True)

class Image (models.Model):
    hid= models.IntegerField(default=0)
    url = models.URLField(max_length=300,default="")
    img = models.ForeignKey(Hotel)

class Comment (models.Model):
    hid= models.IntegerField(default=0)
    com=models.ForeignKey(Hotel)
    text = models.TextField(default="")
