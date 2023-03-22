from django.urls import path
from . import views

app_name = 'item_library'

urlpatterns = [
	path('', views.index, name='index'),
	path('new/', views.new_item, name='item-create'),
	# path('<int:pk/delete/>', views.ItemDeleteView.as_view(), name='item-delete'),
	]