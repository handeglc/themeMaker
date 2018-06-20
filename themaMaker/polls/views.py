from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
import re
from . import models
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def index(request):
	c={};
	return render(request,'index.html',c)

def uploadfun(request):

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
		return render(request,'more.html', {"files": file_list })

def colors(request):
	pass
	
	#return render(request,'more.html',c)
	
	'''files=request.FILES.getlist("filee")
	print("................................................................................................................")
	print(files)
	color_list=[]
	for file in files:
		with open(file.name, newline='') as myFile:
			colors = re.findall(r'color:\s(#[a-zA-Z0-9]*|[a-z]*)',myFile.read(), re.DOTALL)
		color.list.append(colors)
	
	return JsonResponse({"colors": color_list})
	'''