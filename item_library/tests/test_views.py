from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from item_library.models import Item
from item_library.views import FILTERS, DEFAULT_SESSION_KEYS


class ItemLibraryViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("testuser", password="testing321")

        cls.item = Item(title="Spear", 
                        description="A shiny spear", 
                        value=250, 
                        rarity=1, 
                        author=cls.user)

        cls.item.save()

    def setUp(self):
        self.client = Client()
        self.login_successful = self.client.login(username="testuser", 
                                                  password="testing321")
        self.assertTrue(self.login_successful)

    def test_index_view_response(self):
        response = self.client.get(reverse('item_library:index'), follow=True)
        response_content = str(response.content)

        self.assertEqual(200, response.status_code)
        # Check is everything is dispayed
        self.assertIn(self.item.title, response_content)
        self.assertIn(self.item.description, response_content)
        # In database rarity is saved as 1, but it is displayed as Common
        self.assertIn("Common", response_content)

    def test_index_view_default_session_keys(self):
        response = self.client.get(reverse('item_library:index'), follow=True)
        session_keys = self.client.session.keys()

        for f in FILTERS:
            self.assertIn(f, session_keys)

        for d in DEFAULT_SESSION_KEYS.keys():
            self.assertIn(d, self.client.session.keys())
