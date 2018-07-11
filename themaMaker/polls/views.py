from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
import re
import webcolors
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from polls.models import *
from polls import color
from django.template.loader import render_to_string
from .suggestions import update_clusters
from django.contrib.auth.decorators import login_required
from random import randint,choice
from django.core.management import call_command

class UploadView(View):

	def post(self, request, *args, **kwargs):

		files=request.FILES.getlist("filee")
		file_list=[]
		for f in files:
			instance = File(name_field=f.name ,file_field=f)
			instance.save()
			
			with open('/Users/hande/Desktop/Project/themaMaker/uploads/'+f.name, newline='') as myFile:
				colors = re.findall(r'color:\s(#[a-zA-Z0-9]*|[a-z]*)',myFile.read(), re.DOTALL)

			colors = [elem for elem in colors if (elem != "transparent")]

			for x in range(0,len(colors)):
				if ( colors[x][0] != '#'):
					temp = webcolors.html5_parse_legacy_color(colors[x])
					temp_r = str(hex(temp.red))[2:] if(len(str(hex(temp.red)))==4) else ('0'+ str(hex(temp.red))[2])
					temp_g = str(hex(temp.green))[2:] if(len(str(hex(temp.green)))==4) else ('0'+ str(hex(temp.green))[2])
					temp_b = str(hex(temp.blue))[2:] if(len(str(hex(temp.blue)))==4) else ('0'+ str(hex(temp.blue))[2])
					colors[x] = '#' + temp_r + temp_g + temp_b

				elif ( len(colors[x]) < 7 ):
					temp_r = colors[x][1]
					temp_g = colors[x][2]
					temp_b = colors[x][3]
					colors[x] = '#'+ temp_r + temp_r + temp_g + temp_g + temp_b + temp_b

			color_no_list = list(range(len(colors)))
			file_list.append({"name": f.name, "color_list":colors, "color_no_list": color_no_list })

		return render(request,'more.html', {"files": file_list })

class LoginView(View):

	def liked_cg(self,request):
		c={};
		c["liked_cg"]=[]
		if request.user.is_authenticated:
			#c["liked_cg"]
			cg_list =[]
			user_nname = request.user.username
			user_obj = User.objects.get(username = user_nname)
			user = User_Profile.objects.get(user = user_obj)
			cgs = user.liked_color_groups.all()
			for cg in cgs:
				cols = cg.colors.all()
				cols_id = cg.id
				col_list = []
				for c in cols:
					col_list.append(c)
				cg_list.append({"id": cols_id, "list" :col_list})
			
			c = {"liked_cg":cg_list}
		return c
		#return c

	def get(self, request):
		c = self.liked_cg(request)
		return render(request,'login.html',c)

	def post(self, request, *args, **kwargs):
		c = {}
		username = request.POST['username']
		password = request.POST['password']

		user = User.objects.filter(username= username)
		if user.count() == 0:
			c["message"] = "There is not such a user with username: "+ username
		else:
			user = authenticate(request, username=username, password=password)
			
			if user is not None:
				login(request, user)
				#c = self.liked_cg(request)
				print(c)
				c["message"] = "done"
				print(c)
				#return render(request,'index.html',c)
			else:
				c["message"] = "Your username or password is wrong, try again!"
				#return render(request,'login.html',c)
		return JsonResponse(c)


def logout_view(request):
    logout(request)
    return JsonResponse({"successfully_logged_out": "yes"})


def delete_cg_view(request):
	user_nname = request.user.username
	user_obj = User.objects.get(username = user_nname)
	user = User_Profile.objects.get(user = user_obj)
	cg_id = int(request.POST["id"])
	color_set = Color_Groups.objects.filter(id=cg_id)
	user.liked_color_groups.remove(color_set[0])

	return JsonResponse({"saved": "deleted"})


class SaveView(View):

	def get_color_hex_list(self,request):
		data = request.POST.get("datas",None);

		colors = re.findall(r'favcolor=%23([a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9])',data, re.DOTALL) #color hexes but without "#"
		colors_hex = [ "#"+elem for elem in colors] #add '#' to the beginning of the color codes
		return colors_hex

	def post(self, request, *args, **kwargs):
		
		colors_hex = self.get_color_hex_list(request)
		color_set = Color_Groups(how_many_colors=len(colors_hex), group_tendency=color.cg_group_tendency(colors_hex))
		color_set.save()
		for color_hex in colors_hex:
			database_color = Color.objects.filter(color_id_hex=color_hex)
			if database_color.count() == 0:
				color_dic = {"color_id_hex": color_hex,"color_tendency": color.color_tendency(color_hex), "is_light": color.color_is_light(color_hex), "is_saturated":color.color_is_saturated(color_hex)}
				c = Color(**color_dic)
				c.save()
			else:
				c = database_color[0]
			color_set.colors.add(c)


		if request.user.is_authenticated:
			user_nname = request.user.username
			user_obj = User.objects.get(username = user_nname)
			user = User_Profile.objects.get(user = user_obj)
			user.liked_color_groups.add(color_set)

		#update_clusters()
			
		return JsonResponse({"done": data})


class SignUpView(View):
	def post(self, request, *args, **kwargs):

		username = request.POST['username']
		password = request.POST['password']

		taken_name = User.objects.filter(username=username)

		if taken_name.count() == 0:
			user_obj = User.objects.create_user(username=username,email=None,password=password)
			user_obj.save()
			user = User_Profile(user=user_obj)
			user.save()
			us = authenticate(request, username=username, password=password)
			login(request, us)
			return JsonResponse({"saved": "registered"})

		else:
			return JsonResponse({"saved": "same_name_taken"})


class RecommendationView(View):
	def post(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.POST["which"] == "locked_recom": #make recommendation according to locked colors
				print(request.POST["locked"])
				print("oki doki")
				return self.locked_recom(request)
				#return JsonResponse({'username': "",'color_list': ""})
			else:
				return self.user_recommendation_list(request)
		else:
			return JsonResponse({'username': "",'color_list': ""})

	def locked_recom(self,request):
		# get locked colors and process them
		s = SaveView()
		colors_hex = SaveView.get_color_hex_list(s,request)
		print(colors_hex)
		locked = request.POST["locked"]
		locked = list(filter(lambda x: (x != "[") and (x!="]") and (x !="'") and (x!=",") and (x!=" ") and (x!='"'), locked))
		locked_color_indexes = [int(t) for t in locked]
		print(locked_color_indexes)
		locked_colors = [colors_hex[t] for t in locked_color_indexes]
		print(locked_colors)

		# get clusters of clors
		clusters = []
		for c in locked_colors:
			if (Color.objects.filter(color_id_hex=c).count() != 0):
				color_obj = Color.objects.get(color_id_hex=c)
				color_cluster = set(color_obj.color_cluster_set.all())
				print(color_cluster)
			else: #if the color doesn't exist in db
				color_obj = Color(color_id_hex = c, is_light= color.color_is_light(c), is_saturated= color.color_is_saturated(c), color_tendency = color.color_tendency(c))
				color_obj.save()
				color_cluster = set()
				
			clusters.append(color_cluster)
		
		# find the common clusters
		mutual_clusters = set.intersection(*clusters)
		print("mutual: --------------------------")
		print(mutual_clusters)

		# if there is no mutual cluster, update color clusters
		if len(mutual_clusters) == 0:
			call_command('recom')
			return self.user_recommendation_list(request)

		# get all the colors in mutual_clusters in nested list. !!! redundant work here fix later
		recommended_color_lists = [cluster.colors.all() for cluster in mutual_clusters]
		print(recommended_color_lists)
		# select a random color cluster
		color_list_pre = [color.color_id_hex for color in recommended_color_lists[randint(0,len(recommended_color_lists)-1)]]
		print("############################")
		#select random colors from the selected_cluster
		color_list = [color_list_pre[randint(0,len(color_list_pre)-1)] for i in range(0,8)]
		print(color_list)
		return JsonResponse({'username': request.user.username ,'color_list': color_list})

	
	def user_recommendation_list(self,request):

		# get request user reviewed colors
		user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('color')
		user_reviews_color_ids = set(map(lambda x: x.color.id, user_reviews))

	    # get request user cluster name (just the first one righ now)
		try:
			#update_clusters()
			user_cluster_name = \
				User.objects.get(username=request.user.username).cluster_set.first().name
		except: # if no cluster assigned for a user, update clusters
			update_clusters()
			user_cluster_name = \
				User.objects.get(username=request.user.username).cluster_set.first().name
	    
		# get usernames for other memebers of the cluster
		user_cluster_other_members = \
			Cluster.objects.get(name=user_cluster_name).users \
				.exclude(username=request.user.username).all()
		other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

		# get reviews by those users, excluding colors reviewed by the request user
		other_users_reviews = \
			Review.objects.filter(user_name__in=other_members_usernames) \
				.exclude(color__id__in=user_reviews_color_ids)
		other_users_reviews_color_ids = set(map(lambda x: x.color.id, other_users_reviews))

		# then get a color list including the previous IDs, order by rating
		color_list = sorted(
			list(Color.objects.filter(id__in=other_users_reviews_color_ids)), 
			key=lambda x: int(x.average_rating()), 
			reverse=True
		)
		##############################################
		if len(color_list) > 8:
			temp = []
			length = len(color_list)
			while len(temp) < 8:
				c = color_list[randint(0,length-1)]
				if c not in temp:
					temp.append(c)

			color_list = temp
		##############################################
		color_hex_list = [color.color_id_hex for color in color_list]

		if(len(color_hex_list)==0):
			color_hex_list = [self.random_color() for i in range(0,5)]
		##############################################

		return JsonResponse( 
			{'username': request.user.username,'color_list': color_hex_list}
		)

	def random_color(self):
		limit = Color.objects.count()
		c = Color.objects.filter(id=randint(1,limit))
		
		return c[0].color_id_hex
	