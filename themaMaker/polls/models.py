from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
import numpy as np


class Color(models.Model): #color hsl and rgb values can be stored too
	color_id_hex = models.CharField(max_length=30, unique=True, default="", null=False)
	color_name = models.CharField(max_length=100, default="")
	is_light = models.BooleanField(default=True)
	color_tendency = models.CharField(max_length=10, default="")
	is_saturated = models.BooleanField(default=True)

	def __str__(self):
		return (self.color_id_hex +" "+ str(self.color_name))

	def average_rating(self):
		all_ratings = list(map(lambda x: x.rating, self.review_set.all()))
		return np.mean(all_ratings)


class Color_Groups(models.Model):
	colors = models.ManyToManyField(Color)
	how_many_colors = models.IntegerField(default=0)
	group_tendency = models.CharField(max_length=10, default="")

	def __str__(self):
		return (str(self.how_many_colors) +" "+ str(self.group_tendency))


class User_Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
	liked_color_groups = models.ManyToManyField(Color_Groups, blank=True)

	def __str__(self):
		#user_obj = User.objects.get()
		return (self.user.username)

class Review(models.Model):
	RATING_CHOICES = (
		(1, '1'),
		(2, '2'),
		(3, '3'),
		(4, '4'),
		(5, '5'),
	)
	color = models.ForeignKey(Color, on_delete=models.CASCADE)
	user_name = models.CharField(max_length=100)
	rating = models.IntegerField(choices=RATING_CHOICES)

	def __str__(self):
		#user_obj = User.objects.get()
		return (str(self.color.color_id_hex)+" "+ str(self.rating))

class Cluster(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def get_members(self):
        return "\n".join([u.username for u in self.users.all()])

class File(models.Model):
	name_field = models.CharField(max_length=100)
	file_field = models.FileField(upload_to='uploads/')

	def __str__(self):
		return (self.name_field)
