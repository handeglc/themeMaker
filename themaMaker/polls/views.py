from django.shortcuts import render
from django.http import HttpResponse


def index(request):
	c={};
	return render(request,'index.html',c)

def uploadfun(request):
	c={};
	#return render(request,'more.html',c)
	return HttpResponse("heeeeeeey")
