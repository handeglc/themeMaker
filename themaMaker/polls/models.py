from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User




class Color(models.Model): #color hsl and rgb values can be stored too
	color_id_hex = models.CharField(max_length=30)
	color_name = models.CharField(max_length=100, default="")
	is_dark = models.BooleanField(default=True)


class Color_Groups(models.Model):
	colors = models.ManyToManyField(Color)
	how_many_colors = models.IntegerField(default=0)
	tendency = models.CharField(max_length=10, default="")

class User_Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	liked_color_groups = models.ManyToManyField(Color_Groups)

class File(models.Model):
    name_field = models.CharField(max_length=100)
    file_field = models.FileField(upload_to='uploads/')


admin.site.register(File)
admin.site.register(Color)
admin.site.register(Color_Groups)
admin.site.register(User_Profile)

