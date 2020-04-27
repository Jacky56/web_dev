from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from . import models
from PIL import Image

# create custom form
class CustomUserCreationForm(UserCreationForm):

    # add forms with Email Field
    # email = forms.EmailField(required=False)

    username = UsernameField(
        label="Username",
        strip=False,
        widget=forms.TextInput(attrs={'id': 'Username'}),
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'id': 'Password'}),
    )

    # id/classes can have spaces
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'id': 'Password confirmation'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    # this is columns in the User table
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    # override save method
    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        # user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label="Username",
        strip=False,
        widget=forms.TextInput(attrs={'id': 'Username' ,'autofocus': 'autofocus'}),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'id': 'Password'}),
    )


class UploadFileForm(forms.ModelForm):
    x = 0
    y = 0
    width = 0
    height = 0
    size = 0

    class Meta:
        model = models.UploadImagesNN
        fields = ("image",)

    def save(self, commit=True):
        upload = super(UploadFileForm, self).save()

        x = self.x
        y = self.y
        w = self.width
        h = self.height
        size = self.size
        image = Image.open(upload.image)

        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((size, size), Image.ANTIALIAS)
        resized_image.save(upload.image.path)

        return upload








