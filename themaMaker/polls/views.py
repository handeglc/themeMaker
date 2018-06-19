from django.shortcuts import render
from django.http import HttpResponse


def index(request):
	c={};
	return render(request,'index.html',c)

'''def more(request):
	c={};
	print("hayat neden şekil yapıyor")
	return render(request,'more.html',c)
'''