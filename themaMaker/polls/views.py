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
		for f in files:
			instance = models.File(name_field=f.name ,file_field=f)
			instance.save()

			color_list=[]
			for file in files:
				#default_storage.open(f).read()
				with open('/Users/hande/Desktop/Project/themaMaker/uploads/'+f.name, newline='') as myFile:
					colors = re.findall(r'color:\s(#[a-zA-Z0-9]*|[a-z]*)',myFile.read(), re.DOTALL)
				color_list.append(colors)

		return JsonResponse({"colors": color_list})
		#return HttpResponseRedirect('/polls')
	else:
		form = UploadFileForm()
	return render(request, 'upload.html', {'form': form})
	
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