from django.contrib import admin

from tinymce.widgets import TinyMCE
from django.db import models
from .models import SomeCategory, SomeSeries, SomeContext, UserProfile


# Register your models here.

# can reorganise layout on admin page
# only fieldsets or fields can be set
class some_layout_thing(admin.ModelAdmin):
    # reorders stuff
    # fields = ["title",
    #           "published",
    #           "content"]

    # literally pimps out the layout on admin page
    # fieldsets = [
    #     ("divider name", {"fields": ["title", "published"]}),
    #     ("another divider name", {"fields": ["content"]})
    # ]

    # use someone else's plugin and append to your work.
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE(mce_attrs={
            "extended_valid_elements":
                "img[class=responsive-img materialboxed|src|width|height|id],"
                + "iframe[width=100%|class|src|height|id]"
        })
        }
    }


# you need to register your table to make it appear on profile
admin.site.register(SomeContext, some_layout_thing)
admin.site.register(SomeCategory, some_layout_thing)
admin.site.register(SomeSeries, some_layout_thing)
admin.site.register(UserProfile)
