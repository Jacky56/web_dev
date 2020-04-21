from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site

def template1(request):
    url = 'http://' + get_current_site(request).domain
    return """
    <div>
    <button onclick="window.location.href = 'http://127.0.0.1:8000/ye';">ye?</button>
    <button onclick="window.location.href = '{}';">home?</button>
    </div>
    """.format(url)

