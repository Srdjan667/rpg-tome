from django.urls import path
from . import views
from .views import ItemDetailView

app_name = 'item_library'

urlpatterns = [
	path('', views.index, name='index'),
	path('new/', views.new_item, name='item-create'),
	path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
	# path('<int:pk/delete/>', views.ItemDeleteView.as_view(), name='item-delete'),
	]