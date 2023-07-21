from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from item_library.models import Item
from item_library.views import FILTERS, DEFAULT_SESSION_KEYS


class ItemLibraryViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("testuser", password="testing321")

        cls.common_item = Item(title="Spear", 
                               description="A shiny spear", 
                               value=250, 
                               rarity=1, 
                               date_created=timezone.now(),
                               author=cls.user)

        cls.rare_item = Item(title="Magic Wand", 
                             description="A magical wand", 
                             value=2000, 
                             rarity=3, 
                             date_created=timezone.now(), 
                             author=cls.user)

        time = timezone.now() + timedelta(days=30)
        cls.future_item = Item(title="Axe", 
                               description="Axe from future", 
                               date_created=time,
                               author=cls.user)

        cls.common_item.save()
        cls.rare_item.save()
        cls.future_item.save()

    def setUp(self):
        self.client = Client()
        self.login_successful = self.client.login(username="testuser", 
                                                  password="testing321")
        self.assertTrue(self.login_successful)

    def test_index_view_response(self):
        response = self.client.get(reverse('item_library:index'))

        self.assertEqual(200, response.status_code)

    def test_index_view_is_item_displayed(self):
        response = self.client.get(reverse('item_library:index'))
        response_content = str(response.content)

        self.assertIn(self.common_item.title, response_content)
        self.assertIn(self.common_item.description, response_content)

    def test_index_view_is_future_item_displayed(self):
        response = self.client.get(reverse('item_library:index'))
        response_content = str(response.content)

        # Items whose date_created is in future should not be displayed 
        self.assertNotIn(self.future_item.title, response_content)
        self.assertNotIn(self.future_item.description, response_content)

    def test_index_view_default_session_keys(self):
        response = self.client.get(reverse('item_library:index'))
        session_keys = self.client.session.keys()

        for f in FILTERS:
            self.assertIn(f, session_keys)

        for d in DEFAULT_SESSION_KEYS.keys():
            self.assertIn(d, self.client.session.keys())

        # Make sure none of the values are checked
        for r in self.client.session["rarity_list"]:
            self.assertIsNone(r["is_checked"])

    def test_index_view_is_filter_working(self):
        form_data = {
        "filter": "Filter",
        "rare": "3"
        }

        response = self.client.post(reverse('item_library:index'), 
                                    data=form_data)
        response_content = str(response.content)

        # Only items with "rare" rarity should be displayed
        self.assertNotIn(self.common_item.title, response_content)
        self.assertIn(self.rare_item.title, response_content)
