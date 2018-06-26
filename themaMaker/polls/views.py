from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
import re
from . import models
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views import View
from django.contrib.auth import authenticate, login, logout


'''class IndexView(View):

	def get(self, request):
		c={};
		return render(request,'index.html',c)'''


class UploadView(View):

	def post(self, request, *args, **kwargs):

		files=request.FILES.getlist("filee")
		
		file_list=[]
		for f in files:
			instance = models.File(name_field=f.name ,file_field=f)
			instance.save()
			
			with open('/Users/hande/Desktop/Project/themaMaker/uploads/'+f.name, newline='') as myFile:
				colors = re.findall(r'color:\s(#[a-zA-Z0-9]*|[a-z]*)',myFile.read(), re.DOTALL)

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


'''def uploadfun(request):

	if request.method == 'POST':
		#form = UploadFileForm(request.POST, request.FILES)
		files=request.FILES.getlist("filee")
		#if form.is_valid():
		file_list=[]
		for f in files:
			instance = models.File(name_field=f.name ,file_field=f)
			instance.save()
			
			with open('/Users/hande/Desktop/Project/themaMaker/uploads/'+f.name, newline='') as myFile:
				colors = re.findall(r'color:\s(#[a-zA-Z0-9]*|[a-z]*)',myFile.read(), re.DOTALL)

			file_list.append({"name": f.name, "color_list":colors})


			#for file_no in range(0,size(color_list)):
				#counts_list.append(500/size(color_list[file_no]))

		#return JsonResponse({"files": file_list })
		return render(request,'more.html', {"files": file_list })'''

	
	