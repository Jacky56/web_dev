from django.shortcuts import render
from django.http import HttpResponse
from . import template
# Create your views here.






def homepage(request):
	return HttpResponse("""
	{}
	<h1>hello world</h1>
	<div>yeet</div>
	<div>yeet</div>
	<h2>this is home</h2>
	""".format(template.template1(request)))

	
def ye(request):
	return HttpResponse("""
	{}
	<h1>hye</h1>
	<div>yeet</div>
	<div>yeet</div>
	<h2>this is ye</h2>
	""".format(template.template1(request)))

