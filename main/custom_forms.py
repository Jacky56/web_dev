from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# create custom form
class custom_form(UserCreationForm):

    # add forms with Email Field
    email = forms.EmailField(required=False)


    # this is columns in the User table
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    # override save method
    def save(self, commit=True):
        user = super(custom_form, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

