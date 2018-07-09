import pandas as pd
from django.core.management.base import BaseCommand, CommandError
#from django.db import models
from polls.models import *
from django.contrib.auth.models import User
from random import randint,choice
import string
from polls.color import *
from django.contrib.auth import authenticate
#filename = 'color_data.csv'

#dataframe = pd.read_csv(filename)

#dataframe[]


 
class Command(BaseCommand):
	help = 'Command to do........'

	def random_color(self):
		limit = Color.objects.count()
		c = Color.objects.filter(id=randint(0,limit))
		while (c.count() == 0):
			c = Color.objects.filter(id=randint(0,limit))
		return c[0]

	def id_generator(self,size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(choice(chars) for _ in range(size))

	def add_some_data(self):
		limit = Color.objects.count()
		k =randint(1,limit)
		
		

		new_users = [self.id_generator() for i in range(0,k)]

		cg_list = []
		for i in range(1,70):
			#create cg
			k = randint(1,20)
			color_obj_list = [self.random_color() for i in range(0,k)]
			color_list = [self.random_color().color_id_hex for i in range(0,k)]
			cg = Color_Groups(how_many_colors=len(color_list), group_tendency=cg_group_tendency(color_list))
			cg.save()
			for c in color_obj_list:
				cg.colors.add(c)

			cg_list.append(cg)

		print(cg_list)

		for user_name in new_users:
			#create users
			user_obj = User.objects.create_user(username=user_name, email=None, password='1234abcd')
			user_obj.save()
			user = User_Profile(user=user_obj)
			user.save()
			
			
			k =randint(1,20)
			for i in range(1,k):
				user.liked_color_groups.add(cg_list[randint(1, len(cg_list)-1)])

			
		



	def add_argument(self, parser):
		pass

		

	def handle(self, *args, **options):
		#try:
			# your logic here
		print("I am here")
		colors = Color.objects.all()
		userS = User.objects.filter(username = "sampleUser")
		the_user = User_Profile.objects.filter(user = userS[0])
		cg_of_the_user = the_user[0].liked_color_groups.all()

		#reviews = Review.objects.all()
		all_users = User.objects.all()

		'''for user in all_users:
			try:
				u_profile = User_Profile.objects.filter(user=user)[0]
			except:
				u_profile = User_Profile(user=user)
				u_profile.save()
			cgroups = u_profile.liked_color_groups.all()
			for group in cgroups:
				colors_in = group.colors.all()
				for color in colors_in:
					rev = Review()
					rev.color = color
					rev.user_name = user.username
					rev.rating = 5 
					rev.save()'''

		#self.add_some_data()


					

			#print(Color.objects.annotate(cg_ids=color_cgs()))

		#except Exception as e:
			#CommandError(repr(e))
			#print(e)