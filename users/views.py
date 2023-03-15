from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, CustomLoginForm
from django.contrib.auth.views import LoginView

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"Account has been created for {username}! You may now login.")
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form':form})


# Add success message for new user

class CustomLoginView(LoginView):
	form_class = CustomLoginForm
	template_name='users/login.html'