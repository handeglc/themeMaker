from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
import re
import webcolors
from . import models
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views import View
from django.contrib.auth import authenticate, login, logout




class UploadView(View):

	def post(self, request, *args, **kwargs):

		files=request.FILES.getlist("filee")
		
		file_list=[]
		for f in files:
			instance = models.File(name_field=f.name ,file_field=f)
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


			file_list.append({"name": f.name, "color_list":colors})

		return render(request,'more.html', {"files": file_list })

class LoginView(View):

	def get(self, request):
		c={};
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
    return JsonResponse({"successfully logged out": "yes"})
    #c["message"] = "Please login!"
    #return render(request,'login.html',c)



	
	