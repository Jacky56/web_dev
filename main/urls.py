"""hello_world URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

#for creating custom urls, 
app_name = "main"

urlpatterns = [
	path("", views.homepage, name="homepage"),
	path("category/", views.category_slug_url, name="category"),
	path("register/", views.register, name="register"),
	path("logout/", views.logout_request, name="logout"),
	path("login/", views.login_request, name="login"),
	path("profile/", views.profile, name="profile"),
	path("neural-networks/", views.neural_networks, name="neural-networks"),
	path("category/<slug0>/", views.category_slug_url, name="series"),
	path("category/<slug0>/<slug1>/", views.category_slug_url, name="contents"),
	path("category/<slug0>/<slug1>/<slug2>/", views.category_slug_url, name="content"),
	path("test/", views.testing_stuff, name="test"),
	path("tomkat/", views.tomkat, name="tomkat"),
	path("chris/", views.chris, name="chris"),
]
