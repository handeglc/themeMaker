from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
import re
import webcolors
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views import View
from django.contrib.auth import authenticate, login, logout
from polls.models import *
from polls import color


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

	def get(self, request):
		c={};
		#colors = color.color_database()
		#for i in range(len(colors)):
		#	Color.objects.create('color_id_hex'= colors[i]['color_id_hex'], 'color_name'=colors[i]['color_name'], 'is_light'=colors[i]['is_light'], 'color_tendency' = colors[i]['color_tendency'], 'is_saturated' = colors[i]['is_saturated'])
		return render(request,'login.html',c)

	def post(self, request, *args, **kwargs):
		
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		c = {}
		if user is not None:
			login(request, user)
			c["message"] = "you logged in!"
			return render(request,'login.html',c)
		else:
			c["message"] = "try again!"
			return render(request,'login.html',c)

def logout_view(request):
    logout(request)
    return JsonResponse({"successfully_logged_out": "yes"})
    #c["message"] = "Please login!"
    #return render(request,'login.html',c)

class SaveView(View):
	def post(self, request, *args, **kwargs):
		data = request.POST.get("datas",None);
		#print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		#print(data)
		colors = re.findall(r'favcolor=%23([a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9])',data, re.DOTALL) #color hexes but without "#"
		colors_hex = [ "#"+elem for elem in colors] 
		print("______________________________________")
		print(colors_hex)
		print("______________________________________DONE")
		color_set = Color_Groups(how_many_colors=len(colors_hex), group_tendency=color.cg_group_tendency(colors_hex))
		color_set.save()
		for color_hex in colors_hex:
			database_color = Color.objects.filter(color_id_hex=color_hex)
			if database_color.count() == 0:
				color_dic = {"color_id_hex": color_hex, "is_light": color.color_is_light(color_hex), "is_saturated":color.color_is_saturated(color_hex)}
				c = Color(**color_dic)
				c.save()
			else:
				c = database_color[0]
			color_set.colors.add(c)


		if request.user.is_authenticated:
			user_nname = request.user.username
			user = User_Profile.objects.get(username=user_nname)
			user.liked_color_groups.add(color_set)
		return JsonResponse({"done": data})



	
	