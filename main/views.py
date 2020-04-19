from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.

def homepage(request):
	word =  'http://' + get_current_site(request).domain
	return HttpResponse("""
	<h1>hello world</h1>
	<div>yeet</div>
	<div>yeet</div>
	<h2>this is home</h2>
	<div>{}</div>
	<button onclick="window.location.href = 'http://127.0.0.1:8000/ye';">ye?</button>
	""".format(word, word))

	
def ye(request):
	word =  'http://' + get_current_site(request).domain
	return HttpResponse("""
	<h1>hye</h1>
	<div>yeet</div>
	<div>yeet</div>
	<h2>this is ye</h2>
	<button onclick="window.location.href = '{}';">home?</button>
	""".format(word))