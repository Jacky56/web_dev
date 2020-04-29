from django.test import RequestFactory, TestCase, Client
from django.conf import settings
from .models import SomeContext, SomeCategory, SomeSeries
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.files.uploadedfile import SimpleUploadedFile
# Create your tests here.



class BasicTest(TestCase):

    def setUp(self):
        # used to create a fake request
        self.factory = RequestFactory()


    def test_upload_image(self):
        c = Client()
        with open("{}/main/static/main/images/ye.png", settings.BASE_DIR) as img_file:
            c.post("/not/sure/", {"name": "ye.png", "attachment": img_file})




    def test_new_table(self):
        n_table = SomeContext()
        n_table.title = "ye.png"
        n_table.content = "?"
        n_table.published = datetime.now()
        n_table.save()
        record = SomeContext.objects.get(pk=1)
        self.assertEqual(record, n_table)



    def test_media_root(self):
        print(settings.MEDIA_ROOT)
        print(settings.BASE_DIR)
        print(settings.STATIC_ROOT)
        pass

    def test_one(self):
        print("you need to run ur test cases at terminal")
        print("location: where manage.py is")
        print("syntax: manage.py test <Module>.<File>.<Class>.<Method>")
        print("example: manage.py test main.tests")
        self.assertEqual(1, 1)


    def test_global_variables(self):
        print(settings.HELLO_WORLD)
        self.assertEqual(settings.HELLO_WORLD, "hello world", "hello world failed, please set it correctly at setting.py")




    def can_login(self):
        # example of fake request
        request = self.factory.get("/customer/details")

        user = User.objects.create_user(
            username="jacky",
            password="banh"
        )

        loggedin = authenticate(request, username="jacky", password="banh")
        self.assertEqual(loggedin, user)


    def using_object_raw(self):
        request = self.factory.get("/customer/details")
        category = SomeCategory()
        category.title = "cate"
        category.content = "stuff"
        category.slug = "cate"
        category.save()

        series = SomeSeries()
        series.title = "seri"
        series.content = "series sutff"
        series.slug = "series"
        series.series_category = category
        series.save()

        content = SomeContext()
        content.title = "cont"
        content.content = "bits body"
        content.published = datetime.now()
        content.context_series = series
        content.synopsis = "brief"
        content.slug = "content"
        content.save()

        # to query your table it has to be <app_name>_<table>
        for r in SomeCategory.objects.raw("select * from main_SomeCategory"):
            print(r.title)
            print(r.content)
            print(r.slug)

        print("--------------------")
        # to query your table it has to be <app_name>_<table>
        for r in SomeSeries.objects.raw("select * from main_SomeSeries"):
            print(r.title)
            print(r.content)
            print(r.slug)
            print(r.series_category)

        print("--------------------")

        # to query your table it has to be <app_name>_<table>
        # reference keys must contin suffix _id
        for r in SomeContext.objects.raw("select * from main_SomeContext"):
            print(r.context_series_id)



