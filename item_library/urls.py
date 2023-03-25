from django.urls import path
from . import views
from .views import ItemDetailView, ItemUpdateView, ItemDeleteView

app_name = 'item_library'

urlpatterns = [
	path('', views.index, name='index'),
	path('new/', views.new_item, name='item-create'),
	path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
	path('item/<int:pk>/update/', ItemUpdateView.as_view(), name='item-update'),
	path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),
	]