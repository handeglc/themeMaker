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

	def get(self, request):
		c = self.liked_cg(request)
		return render(request,'login.html',c)

	def post(self, request, *args, **kwargs):
		
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		c = {}
		
		if user is not None:
			login(request, user)
			c = self.liked_cg(request)
			c["message"] = "you logged in!"
			return render(request,'index.html',c)
		else:
			c["message"] = "try again!"
			c = self.liked_cg(request)
			return render(request,'login.html',c)

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
	def post(self, request, *args, **kwargs):
		data = request.POST.get("datas",None);

		colors = re.findall(r'favcolor=%23([a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9])',data, re.DOTALL) #color hexes but without "#"
		colors_hex = [ "#"+elem for elem in colors] #add '#' to the beginning of the color codes
		
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

		update_clusters()
			
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



@login_required
def user_recommendation_list(request):

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
			c = color_list[randint(0,length)]
			if c not in temp:
				temp.append(c)

		color_list = temp
	##############################################
	color_hex_list = [color.color_id_hex for color in color_list]

	if(len(color_hex_list)==0):
		color_hex_list = [random_color() for i in range(0,5)]
	##############################################

	return JsonResponse( 
		{'username': request.user.username,'color_list': color_hex_list}
	)

def random_color():
	limit = Color.objects.count()
	c = Color.objects.filter(id=randint(1,limit))
	
	return c[0].color_id_hex
	