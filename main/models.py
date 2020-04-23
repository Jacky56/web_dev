from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# model map to database table

# Create your models here.

# creates a table in database with these fields


class SomeCategory(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # for URL
    slug = models.SlugField(unique=True, max_length=50)
    image = models.ImageField(upload_to="main/category/images", blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class SomeSeries(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # for URL
    slug = models.SlugField(unique=True, max_length=50)
    series_category = models.ForeignKey(SomeCategory, default=1, verbose_name="Category", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="main/series/images", blank=True)

    class Meta:
        verbose_name_plural = "Series"

    def __str__(self):
        return self.title

# creates a table in database with these fields
class SomeContext(models.Model):
    # column named title
    title = models.CharField(max_length=200)

    synopsis = models.CharField(help_text="provide a synopsis for the content", max_length=200)

    # column named content
    content = models.TextField(default="you can set default value")
    # columned named published
    published = models.DateTimeField("date name ?")
    # for URL
    slug = models.CharField(max_length=50)
    # ForeignKey
    context_series = models.ForeignKey(SomeSeries, default=1, verbose_name="Series", on_delete=models.CASCADE)


    #? replace return type with a readable string
    def __str__(self):
        return self.title


# beware referencing variables in html requires all to be lowercase
class UserProfile(models.Model):
    # allows user object to access this class
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField(max_length=500, blank=True)
    # upload_to is a directory
    avatar = models.ImageField(upload_to="main/avatar", blank=True)

    def __str__(self):
        return self.user.username


# create methods to cascade actions
# creates a user profile when user is created

def create_profile(sender, **kwargs):
    if kwargs["created"]:
        user_profile = UserProfile.objects.create(user=kwargs["instance"])





post_save.connect(create_profile, sender=User)