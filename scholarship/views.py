from django.shortcuts import render
from django.template import Context, loader, Template
from django.http import HttpResponse
from backend import collect
from analyse import analyse,build_markers
from .models import *
import threading,time

from django.db import connection
cursor = connection.cursor()

class collectThread(object):
    def __init__(self, interval=1):
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
    def run(self):
        collect()
        time.sleep(self.interval)

def homepage(request):
	collectThread()
	template= loader.get_template('scholarship/index.html')
	return HttpResponse(template.render(request))

def highchart(request):
	analyse()
	template= loader.get_template('scholarship/highchart.html')
	return HttpResponse(template.render(request))

def map(request):
	build_markers()
	template= loader.get_template('scholarship/map.html')
	return HttpResponse(template.render(request))

def search(request):
	template= loader.get_template('scholarship/search.html')
	category= Scholarship.objects.values('category').distinct()
	country= Scholarship.objects.values('country').distinct()
	university = Scholarship.objects.values('university').distinct()
	context={'all_category':category,
			 'all_country':country,
			 'all_university':university,}
	return HttpResponse(template.render(context,request))

def search_result(request):
	template= loader.get_template('scholarship/result.html')
	try:
		if request.POST.get('category'):
			value=request.POST.get('category')
			result=Scholarship.objects.filter(category=value).distinct()
		elif request.POST.get('country'):
			value=request.POST.get('country')
			result=Scholarship.objects.filter(country=value).distinct()
		elif request.POST.get('university'):
			value=request.POST.get('university')
			result=Scholarship.objects.filter(university=value).distinct()
		return HttpResponse(template.render({'records':result,'value':value},request))
	except Exception as e:
		return HttpResponse(template.render({'error':"No Scholarship Available",'value':''},request))


'''	TO DO
add source link              https://twitter.com/statuses/ID
remove "," from url
add facebook
add back buttons
'''