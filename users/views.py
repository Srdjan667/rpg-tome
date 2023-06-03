from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, CustomLoginForm
from django.contrib.auth.views import *
from django.urls import reverse_lazy

def CustomRegisterView(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request,
				f"Account has been created for {username}, you may now login.")
			return redirect('account:login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form':form})
	

class CustomLoginView(LoginView):
	form_class = CustomLoginForm
	template_name='users/login.html'


class CustomPasswordResetView(PasswordResetView):
	email_template_name = "registration/password_reset_email.html"
	success_url = reverse_lazy("account:password_reset_done")


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
	success_url = reverse_lazy("account:password_reset_complete")

