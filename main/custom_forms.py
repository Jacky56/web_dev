from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User


# create custom form
class CustomUserCreationForm(UserCreationForm):

    # add forms with Email Field
    # email = forms.EmailField(required=False)

    username = UsernameField(
        label="Username",
        strip=False,
        widget=forms.TextInput(attrs={'for': 'Username'}),
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'for': 'Password1'}),
    )

    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'for': 'Password2'}),
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
        widget=forms.TextInput(attrs={'for': 'Username'}),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'for': 'Password'}),
    )



