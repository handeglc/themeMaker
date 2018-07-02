from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class Color(models.Model): #color hsl and rgb values can be stored too
	color_id_hex = models.CharField(max_length=30, unique=True, default="", null=False)
	color_name = models.CharField(max_length=100, default="")
	is_light = models.BooleanField(default=True)
	color_tendency = models.CharField(max_length=10, default="")
	is_saturated = models.BooleanField(default=True)

	def __str__(self):
		return (self.color_id_hex +" "+ str(self.color_name))


class Color_Groups(models.Model):
	colors = models.ManyToManyField(Color)
	how_many_colors = models.IntegerField(default=0)
	group_tendency = models.CharField(max_length=10, default="")

	def __str__(self):
		return (str(self.how_many_colors) +" , "+ str(self.group_tendency))


class User_Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
	liked_color_groups = models.ManyToManyField(Color_Groups, blank=True)

	def __str__(self):
		#user_obj = User.objects.get()
		return (self.user.username)

class File(models.Model):
	name_field = models.CharField(max_length=100)
	file_field = models.FileField(upload_to='uploads/')

	def __str__(self):
		return (self.name_field)
