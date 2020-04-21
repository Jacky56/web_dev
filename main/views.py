from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import template
from .models import new_table
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .custom_forms import custom_form

# Create your views here.



def homepage(request):
	return render(
		request = request,
		template_name = "main/home.html",
	    context = {"tutorials": new_table.objects.all},
	)


def homepage_old(request):
	return HttpResponse("""
	{}
	<h1>hello world</h1>
	<div>yeet</div>
	<div>yeet</div>
	<h2>this is home</h2>
	""".format(template.template1(request)))



def tutorial(request):
	return render(
		request=request,
		template_name="main/tutorial.html",
		context={"tutorials": new_table.objects.all}
	)

def register(request):
	if request.method == "POST":
		#gets info from UserCreationForm or the data from the register page
		form = custom_form(request.POST)
		if form.is_valid():
			# saves to table
			user = form.save()
			username = form.cleaned_data.get("username")
			messages.success(
				request=request,
				message="created account for {}".format(username)
			)
			# maybe just login for you
			login(
				request=request,
				user=user
			)
			return redirect("/")
			# can also be
			# return redirect("main:homepage")
		else:
			for key in form.error_messages:
				messages.error(
					request=request,
					message="{}".format(form.error_messages[key])
				)

	form = custom_form
	return render(
		request=request,
		template_name="main/register.html",
		context={"form": form}
	)


def logout_request(request):
	if request.user.is_authenticated:
		username = request.user.username
		# i think removes current user from request.
		logout(
			request=request
		)
		messages.info(request, "{} logged out!".format(username))
	return redirect("/")

def login_request(request):
	if request.method == "POST":
		# data= gets the data from the request
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			username = form.cleaned_data.get("username")
			messages.success(
				request=request,
				message="welcome back {}".format(username)
			)
			login(
				request=request,
				user=user
			)
			return redirect("/")
		else:
			messages.error(
				request=request,
				message="invalid username or password"
			)


	form = AuthenticationForm
	return render(
		request=request,
		template_name="main/login.html",
		context={"form": form}
	)
