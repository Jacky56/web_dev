from django.test import RequestFactory, TestCase
from django.conf import settings
from .models import SomeContext
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# Create your tests here.



class BasicTest(TestCase):

    def setUp(self):
        # used to create a fake request
        self.factory = RequestFactory()


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






