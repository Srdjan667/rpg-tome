from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

app_name = 'account'

urlpatterns = [
	path('register/', 
		CustomRegisterView, name='register'),

	path('login/', 
		CustomLoginView.as_view(), name='login'),

	path('logout/', 
		LogoutView.as_view(), name='logout'),

	path('password_change/', 
		CustomPasswordChangeView.as_view(), name='password_change'),

	path('password_change/done/', 
		PasswordChangeDoneView.as_view(), name='password_change_done'),

	path('password_reset/', 
		CustomPasswordResetView.as_view(), name='password_reset'),

	path('password_reset/done/', 
		PasswordResetDoneView.as_view(), name='password_reset_done'),

	path('reset/<uidb64>/<token>/', 
		CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

	path('reset/done/', 
		PasswordResetCompleteView.as_view(), name='password_reset_complete'),]