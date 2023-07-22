from django.test import TestCase
from django.contrib.auth.models import User

from item_library.models import Item


class ItemModelTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		user = User.objects.create(username="testuser")
		Item.objects.create(title="Spear", author=user)

	def test_title_label(self):
		item = Item.objects.get(id=1)
		field_label = item._meta.get_field("title").verbose_name
		self.assertEqual(field_label, "title")

	def test_title_max_length(self):
		item = Item.objects.get(id=1)
		max_length = item._meta.get_field("title").max_length
		self.assertEqual(max_length, 100)

	def test_title_is_name(self):
		item = Item.objects.get(id=1)
		expected_name = item.title
		self.assertEqual(str(item), expected_name)
		