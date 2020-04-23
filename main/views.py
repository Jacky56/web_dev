from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import SomeContext, SomeCategory, SomeSeries
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .custom_forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.models import User

from django.conf import settings

# Create your views here.

# manages multiple slug values with **kwargs
def category_slug_url(request, **kwargs):
	href = {"category": "/category/"}
	if kwargs:
		categories = [c.slug for c in SomeCategory.objects.all()]
		if 'slug0' in kwargs:
			if kwargs['slug0'] in categories:
				href[kwargs['slug0']] = "{}{}/".format(href["category"], kwargs['slug0'])
				# you need __ to join on tables
				series = SomeSeries.objects.filter(series_category__slug=kwargs['slug0'])
				series_slugs = [s.slug for s in series.all()]
				if 'slug1' in kwargs:
					if kwargs['slug1'] in series_slugs:
						href[kwargs['slug1']] = "{}{}/".format(href[kwargs['slug0']], kwargs['slug1'])
						contexts = SomeContext.objects.filter(context_series__slug=kwargs['slug1'])
						contexts_slug = [c.slug for c in contexts.all()]
						if 'slug2' in kwargs:
							if kwargs['slug2'] in contexts_slug:
								href[kwargs['slug2']] = "{}{}/".format(href[kwargs['slug1']], kwargs['slug2'])
								context = contexts.filter(slug=kwargs['slug2'])
								return render(
									request=request,
									template_name="main/content.html",
									context={"content": context.all()[0], "href": href, "categories": contexts.all()}
								)
							else:
								messages.error(
									request=request,
									message="{} does not exist.".format(kwargs['slug2'])
								)
								return redirect("../")
						return render(
							request=request,
							template_name="main/category.html",
							context={"categories": contexts.all(), "href": href}
						)
					else:
						messages.error(
							request=request,
							message="{} does not exist.".format(kwargs['slug1'])
						)
						return redirect("../")
				return render(
					request=request,
					template_name="main/category.html",
					context={"categories": series.all(), "href": href}
				)
			else:
				messages.error(
					request=request,
					message="{} does not exist.".format(kwargs['slug0'])
				)
				return redirect("../")
	else:
		return render(
			request=request,
			template_name="main/category.html",
			context={"categories": SomeCategory.objects.all(), "href": href}
		)


def homepage(request):
	return render(
		request = request,
		template_name = "main/home.html",
	)


def tomkat(request):
	return render(
		request = request,
		template_name = "main/tomkat.html",
	)


def profile(request):
	return render(
		request=request,
		template_name="main/profile.html",
		context={"user": request.user}
	)


def register(request):
	if request.method == "POST":
		#gets info from UserCreationForm or the data from the register page
		form = CustomUserCreationForm(request.POST)
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

	form = CustomUserCreationForm
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


# delete
def testing_stuff(request):
	return render(
		request,
		template_name="main/test.html",
		context={ "nums": range(10)}
	)


def login_request(request):
	if request.method == "POST":
		# data= gets the data from the request
		form = CustomAuthenticationForm(request, data=request.POST)
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

	form = CustomAuthenticationForm
	return render(
		request=request,
		template_name="main/login.html",
		context={"form": form}
	)


def neural_networks(request):
	return render(
		request=request,
		template_name="main/neural-networks.html",
	)