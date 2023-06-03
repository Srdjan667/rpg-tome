from django.test import TestCase
from django.utils import timezone
import datetime
from .models import Item

class ItemModelTests(TestCase):
	def test_was_published_recently_with_future_item(self):
		"""
		was_published_recently() returns False for items whose date_created
		is in the future.
		"""
		time = timezone.now() + datetime.timedelta(
								days=30)

		future_item = Item(date_created=time)
		self.assertIs(future_item.was_published_recently(), False)

	def test_was_published_recently_with_old_item(self):
		"""
		was_published_recently() returns False for items whose date_created
		is older than 1 day.
		"""
		time = timezone.now() - datetime.timedelta(
								days=1, seconds=1)

		old_item = Item(date_created=time)
		self.assertIs(old_item.was_published_recently(), False)

	def test_was_published_recently_with_recent_item(self):
		"""
		was_published_recently() returns True for items whose date_created
		is within the last day.
		"""
		time = timezone.now() - datetime.timedelta(
								hours=23, minutes=59,seconds=59)

		recent_item = Item(date_created=time)
		self.assertIs(recent_item.was_published_recently(), True)

	def test_was_modified_recently_with_future_item(self):
		"""
		was_modified_recently() returns False for items whose last_modified 
		is in the future.
		"""
		time = timezone.now() + datetime.timedelta(
								days=30)

		future_item = Item(last_modified=time)
		self.assertIs(future_item.was_modified_recently(), False)

	def test_was_modified_recently_with_old_item(self):
		"""
		was_modified_recently() returns False for items whose last_modified 
		is older than 1 day.
		"""
		time = timezone.now() - datetime.timedelta(
								days=1, seconds=1)

		old_item = Item(last_modified=time)
		self.assertIs(old_item.was_modified_recently(), False)

	def test_was_modified_recently_with_recent_item(self):
		"""
		was_modified_recently() returns True for items whose last_modified 
		is within the last day.
		"""
		time = timezone.now() - datetime.timedelta(
								hours=23, minutes=59, seconds=59)

		recent_item = Item(last_modified=time)
		self.assertIs(recent_item.was_modified_recently(), True)
