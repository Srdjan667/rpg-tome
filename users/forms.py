from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _

class UserRegisterForm(UserCreationForm):
	username = forms.CharField(
		label=_(""),
		widget=forms.TextInput(attrs={"autocomplete": "username", "placeholder": "Username"}), 
		help_text=None
		)

	email = forms.EmailField(
		label=_(""),
		widget=forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "Email"}), 
		help_text=None
		)

	password1 = forms.CharField(
		label=_(""),
		widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "placeholder": "Password"}), 
		help_text=None,
	)

	password2 = forms.CharField(
		label=_(""),
		widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "placeholder": "Confirm Password"}),
		help_text=None,
	)

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class CustomLoginForm(AuthenticationForm):
	username = forms.CharField(
		label=_(""),
		widget=forms.TextInput(attrs={"autofocus": True, 'placeholder': 'Username'}))

	password = forms.CharField(
		label=_(""),
		strip=False,
		widget=forms.PasswordInput(attrs={"autocomplete": "current-password", 'placeholder': 'Password'}),
	)
