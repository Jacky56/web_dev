from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import SomeContext, SomeCategory, SomeSeries, UploadImagesNN, cv
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .custom_forms import CustomUserCreationForm, CustomAuthenticationForm, UploadFileForm
from django.contrib.auth.models import User
import numpy as np
from PIL import Image
from .apps import MainConfig
from .functions import Functions
import tensorflow as tf

global graph
graph = tf.get_default_graph()
global f
f = Functions()

# Create your views here.

# this version will reset url if user place strange values
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

# manages multiple slug values with **kwargs
def category_slug_url1(request, **kwargs):
	href = {"category": "/category/"}
	if kwargs:
		categories = [c.slug for c in SomeCategory.objects.all()]
		value = f.find_slug(categories, 'slug0', kwargs)
		if value:
			href[kwargs['slug0']] = "{}{}/".format(href["category"], kwargs['slug0'])
			# you need __ to join on tables
			series = SomeSeries.objects.filter(series_category__slug=kwargs['slug0'])
			series_slugs = [s.slug for s in series.all()]
			value = f.find_slug(series_slugs, 'slug1', kwargs)
			if value:
				href[kwargs['slug1']] = "{}{}/".format(href[kwargs['slug0']], kwargs['slug1'])
				contexts = SomeContext.objects.filter(context_series__slug=kwargs['slug1'])
				contexts_slug = [c.slug for c in contexts.all()]
				value = f.find_slug(contexts_slug, 'slug2', kwargs)
				if value:
					href[kwargs['slug2']] = "{}{}/".format(href[kwargs['slug1']], kwargs['slug2'])
					context = contexts.filter(slug=kwargs['slug2'])
					return render(
						request=request,
						template_name="main/content.html",
						context={"content": context.all()[0], "href": href, "categories": contexts.all()}
					)
				return render(
					request=request,
					template_name="main/category.html",
					context={"categories": contexts.all(), "href": href}
				)
			return render(
				request=request,
				template_name="main/category.html",
				context={"categories": series.all(), "href": href}
			)
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
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			# tmp_img = form.save(commit=False)
			# get raw binary image
			# raw_img = request.FILES["image"]
			uploaded_img = form.cleaned_data.get("image")
			#converts raw image to np.array
			# image_file = StringIO(str(raw_img.read()))

			# img = cv2.imdecode(np.fromstring(raw_img.read(), np.uint8), cv2.IMREAD_UNCHANGED)
			img = Image.open(uploaded_img.file.name)

			img = f.down_size_image(img, 720)

			# loads model for detecting face
			# haar_cascade_face = MainConfig.FACE_DETECTOR
			# faces_rects = haar_cascade_face.detectMultiScale(np.array(img), scaleFactor=1.1, minNeighbors=5)

			with graph.as_default():
				faces_rects = MainConfig.FACE_DETECTOR.detect_faces(np.array(img)[:, :, :3])

			if len(faces_rects) > 0:
				img = f.get_face(img, 64, faces_rects)

				# grab image details
				file_img = uploaded_img.file
				# saving image
				img.save(file_img, format="PNG")
				uploaded_img.file = file_img
				final_img = form.save()

				# predicting with model
				with graph.as_default():
					# ins = img_to_array(load_img(final_img.image.path))
					prediction = MainConfig.MODEL.predict(np.array([np.array(img)[:, :, :3]/255.]))
					attributes = f.format_predictions(prediction[0], MainConfig.LABELS)

					return HttpResponse(
						"""
						<p>{}</p>
						<img src="{}" />
						{}

						{}
						""".format(final_img.image.url, final_img.image.url,  attributes, final_img.image.path)
				)
			else:
				messages.error(
					request=request,
					message="Cant find any faces!"
				)

	form = UploadFileForm

	return render(
		request,
		template_name="main/test.html",
		context={"form": form}
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

	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():

			#get img data
			uploaded_img = form.cleaned_data.get("image")

			#convert to pillow.Image
			img = Image.open(uploaded_img.file.name)

			#makes img small if too big
			img = f.down_size_image(img, 720)


			with graph.as_default():
				#grab face
				faces_rects = MainConfig.FACE_DETECTOR.detect_faces(f.to_np_image(img))

			if len(faces_rects) > 0:
				if len(faces_rects) > 1:
					messages.info(
						request=request,
						message="There's like {} faces in that photo, picking the first one.".format(len(faces_rects))
					)
				#get face from landmarks
				img = f.get_face(img, 64, faces_rects)

				# grab image details
				file_img = uploaded_img.file
				# saving image
				img.save(file_img, format="PNG")
				uploaded_img.file = file_img
				final_img = form.save()

				# predicting with model
				with graph.as_default():
					#classify image
					prediction = MainConfig.MODEL.predict(np.array([f.to_np_image(img)/255.]))
					attributes = f.format_predictions(prediction[0], MainConfig.LABELS)
					return render(
						request=request,
						template_name="main/neural-networks.html",
						context={"form": form, "attributes": attributes, "image_face": final_img}
					)

			else:
				messages.error(
					request=request,
					message="Can't find any faces!"
				)

	form = UploadFileForm
	return render(
		request=request,
		template_name="main/neural-networks.html",
		context={"form": form}
	)


def tomkat(request):
	return render(
		request = request,
		template_name = "main/tomkat.html",
	)

def chris(request):
	return render(
		request = request,
		template_name = "main/chris.html",
	)

def info(request):
	cv_data = cv.objects.all()[0]

	return render(
		request=request,
		template_name="main/info.html",
		context={"cv": cv_data}
	)