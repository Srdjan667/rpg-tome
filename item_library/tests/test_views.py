import re
from datetime import timedelta
from random import randint

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from item_library.models import Item
from item_library.views import ITEMS_PER_PAGE


class ItemLibraryViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testing321")

        cls.common_item = Item(
            title="Spear",
            description="A shiny spear",
            value=250,
            rarity=1,
            date_created=timezone.now(),
            author=cls.user,
        )

        cls.rare_item = Item(
            title="Magic Wand",
            description="A magical wand",
            value=2000,
            rarity=3,
            date_created=timezone.now(),
            author=cls.user,
        )

        time = timezone.now() + timedelta(days=30)
        cls.future_item = Item(
            title="Axe",
            description="Axe from future",
            date_created=time,
            author=cls.user,
        )

        cls.common_item.save()
        cls.rare_item.save()
        cls.future_item.save()

    def setUp(self):
        self.client = Client()
        self.login_successful = self.client.login(
            username="testuser", password="testing321"
        )
        self.assertTrue(self.login_successful)

    def test_index_view_response(self):
        response = self.client.get(reverse("item_library:index"))

        self.assertEqual(200, response.status_code)

    def test_index_view_is_item_displayed(self):
        response = self.client.get(reverse("item_library:index"))
        response_content = str(response.content)

        self.assertIn(self.common_item.title, response_content)
        self.assertIn(self.common_item.description, response_content)

    def test_index_view_is_future_item_displayed(self):
        response = self.client.get(reverse("item_library:index"))
        response_content = str(response.content)

        # Items whose date_created is in future should not be displayed
        self.assertNotIn(self.future_item.title, response_content)
        self.assertNotIn(self.future_item.description, response_content)

    def test_index_view_is_filter_working(self):
        form_data = {"submit": "", "rare": "on"}

        response = self.client.get(reverse("item_library:index"), data=form_data)
        response_content = str(response.content)

        # Only items with "rare" rarity should be displayed
        self.assertNotIn(self.common_item.title, response_content)
        self.assertIn(self.rare_item.title, response_content)


class ItemLibrarySortingTest(TestCase):
    URL_NAME = "item_library:index"

    @classmethod
    def setUpTestData(cls):
        # Create user
        cls.user = User.objects.create_user("testuser", password="testing321")

        item_name = "Item"

        # Create enough items for one page with random values
        for i in range(ITEMS_PER_PAGE):
            create_item = Item(
                title=f"{item_name}{i}",
                value=randint(1, 50000),
                rarity=randint(1, 5),
                author=cls.user,
            )
            create_item.save()

    def setUp(self):
        # Create client for interacting with view
        self.client = Client()
        self.login_successful = self.client.login(
            username="testuser", password="testing321"
        )
        self.assertTrue(self.login_successful)

    def fetch_items_from_database(self, order):
        # Fetch items from the database and order them
        items = Item.objects.all().order_by(order)

        # Return a list of their titles
        return [item.title for item in items]

    def find_items_in_html(self, response):
        # Find all items returned by client
        pattern = re.compile(r"<h5 class=\"mb-1\">(.*?)</h5>")
        return re.findall(pattern, response)

    def get_response(self, form_data):
        response = self.client.get(reverse(self.URL_NAME), data=form_data)
        return response

    def test_index_view_is_date_created_order_working(self):
        # Simulate user sorting items by the time they were created
        form_data = {"submit": "", "order": "date_created", "direction": "ascending"}

        response = self.get_response(form_data)

        database_items = self.fetch_items_from_database("date_created")
        html_items = self.find_items_in_html(response.content.decode("utf-8"))

        # Compare items from database with those generated in HTML
        self.assertEqual(database_items, html_items)

    def test_index_view_is_title_order_working(self):
        # Simulate user sorting items by their titles
        form_data = {"submit": "", "order": "title", "direction": "ascending"}

        response = self.get_response(form_data)

        database_items = self.fetch_items_from_database("title")
        html_items = self.find_items_in_html(response.content.decode("utf-8"))

        # Compare items from database with those generated in HTML
        self.assertEqual(database_items, html_items)

    def test_index_view_is_rarity_order_working(self):
        # Simulate user sorting items by their rarities
        form_data = {"submit": "", "order": "rarity", "direction": "ascending"}

        response = self.get_response(form_data)

        database_items = self.fetch_items_from_database("rarity")
        html_items = self.find_items_in_html(response.content.decode("utf-8"))

        # Compare items from database with those generated in HTML
        self.assertEqual(database_items, html_items)

    def test_index_view_is_value_order_working(self):
        # Simulate user sorting items by their values
        form_data = {"submit": "", "order": "value", "direction": "ascending"}

        response = self.get_response(form_data)

        database_items = self.fetch_items_from_database("value")
        html_items = self.find_items_in_html(response.content.decode("utf-8"))

        # Compare items from database with those generated in HTML
        self.assertEqual(database_items, html_items)


class ItemLibraryFilteringTest(TestCase):
    URL_NAME = "item_library:index"

    @classmethod
    def setUpTestData(cls):
        # Create user
        cls.user = User.objects.create_user("testuser", password="testing321")

        item_name = "Item"

        # Create enough items for one page with random values
        for i in range(ITEMS_PER_PAGE):
            create_item = Item(
                title=f"{item_name}{i}",
                value=randint(1, 50000),
                rarity=randint(1, 5),
                author=cls.user,
            )
            create_item.save()

    def setUp(self):
        # Create client for interacting with view
        self.client = Client()
        self.login_successful = self.client.login(
            username="testuser", password="testing321"
        )
        self.assertTrue(self.login_successful)

    def tearDown(self):
        self.client.logout()

    def fetch_items_from_database(self, **params):
        # Fetch items from the database
        items = Item.objects.filter(**params)
        return [item.title for item in items]

    def find_in_html(self, response):
        # Find all items returned by client
        pattern = re.compile(r"<h5 class=\"mb-1\">(.*?)</h5>")
        return re.findall(pattern, response)

    def get_response(self, form_data):
        response = self.client.get(reverse(self.URL_NAME), data=form_data)
        return response

    def test_index_view_is_title_filter_working(self):
        form_data = {
            "submit": "",
            "title": "item",
        }

        response = self.get_response(form_data)

        # Fetch items from the database that contain title
        params = {"title__icontains": form_data["title"]}
        items_from_database = self.fetch_items_from_database(**params)

        html_items = self.find_in_html(response.content.decode("utf-8"))

        # Compare items from database with those generated in HTML
        self.assertEqual(sorted(items_from_database), sorted(html_items))

    def test_index_view_is_min_value_filter_working(self):
        form_data = {"submit": "", "min_value": randint(1, 50000)}

        response = self.get_response(form_data)

        # Fetch items from the database whose value is equal or greater than
        # min_value
        params = {"value__gte": form_data["min_value"]}
        items_from_database = self.fetch_items_from_database(**params)

        html_items = self.find_in_html(response.content.decode("utf-8"))

        # Compare items from database with those generated in HTML
        self.assertEqual(sorted(items_from_database), sorted(html_items))

    def test_index_view_is_max_value_filter_working(self):
        form_data = {"submit": "", "max_value": randint(1, 50000)}

        response = self.get_response(form_data)

        # Fetch items from the database whose value is less or equal than
        # min_value
        params = {"value__lte": form_data["max_value"]}
        items_from_database = self.fetch_items_from_database(**params)

        html_items = self.find_in_html(response.content.decode("utf-8"))

        # Compare items from database with those generated in HTML
        self.assertEqual(sorted(items_from_database), sorted(html_items))
