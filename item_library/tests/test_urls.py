from django.test import SimpleTestCase
from django.urls import reverse, resolve
from item_library.views import (
	index, new_item, ItemDetailView, ItemUpdateView, ItemDeleteView)


class TestItemLibraryUrls(SimpleTestCase):
	
	def test_index_is_resolved(self):
		url = reverse('item_library:index')
		self.assertEquals(resolve(url).func, index)

	def test_item_create_is_resolved(self):
		url = reverse('item_library:item-create')
		self.assertEquals(resolve(url).func, new_item)

	def test_item_detail_is_resolved(self):
		url = reverse('item_library:item-detail', args=[1])
		self.assertEquals(resolve(url).func.view_class, ItemDetailView)

	def test_item_update_is_resolved(self):
		url = reverse('item_library:item-update', args=[1])
		self.assertEquals(resolve(url).func.view_class, ItemUpdateView)

	def test_item_delete_is_resolved(self):
		url = reverse('item_library:item-delete', args=[1])
		self.assertEquals(resolve(url).func.view_class, ItemDeleteView)