from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView

from . import views

app_name = 'account'

urlpatterns = [
	path('register/', views.register, name='register'),
	path('login/', CustomLoginView.as_view(), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
	]