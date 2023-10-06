import re
from datetime import timedelta
from random import randint

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from library.models import Item
from library.views import ITEMS_PER_PAGE


class ItemLibraryViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testing321")

        cls.objs = Item.objects.bulk_create(
            [
                Item(
                    title="Spear",
                    description="A shiny spear",
                    value=250,
                    rarity=1,
                    date_created=timezone.now(),
                    author=cls.user,
                ),
                Item(
                    title="Magic Wand",
                    description="A magical wand",
                    value=2000,
                    rarity=3,
                    date_created=timezone.now(),
                    author=cls.user,
                ),
                Item(
                    title="Axe",
                    description="Axe from future",
                    date_created=timezone.now() + timedelta(days=30),
                    author=cls.user,
                ),
            ]
        )

    def setUp(self):
        self.client = Client()
        self.login_successful = self.client.login(
            username="testuser", password="testing321"
        )
        self.assertTrue(self.login_successful)

    def test_index_view_response(self):
        response = self.client.get(reverse("library:item-list"))

        self.assertEqual(200, response.status_code)

    def test_index_view_is_item_displayed(self):
        response = self.client.get(reverse("library:item-list"))
        response_content = str(response.content)

        self.assertIn(self.objs[0].title, response_content)
        self.assertIn(self.objs[0].description, response_content)

    def test_index_view_is_future_item_displayed(self):
        response = self.client.get(reverse("library:item-list"))
        response_content = str(response.content)

        # Items whose date_created is in future should not be displayed
        self.assertNotIn(self.objs[2].title, response_content)
        self.assertNotIn(self.objs[2].description, response_content)

    def test_index_view_is_filter_working(self):
        form_data = {"submit": "", "rare": "on"}

        response = self.client.get(reverse("library:item-list"), data=form_data)
        response_content = str(response.content)

        # Only items with "rare" rarity should be displayed
        self.assertNotIn(self.objs[0].title, response_content)
        self.assertIn(self.objs[1].title, response_content)


class ItemLibrarySortingTest(TestCase):
    URL_NAME = "library:item-list"

    @classmethod
    def setUpTestData(cls):
        # Create user
        cls.user = User.objects.create_user(username="testuser", password="testing321")

        item_name = "Item"

        # Create enough items for one page with random values
        for i in range(ITEMS_PER_PAGE):
            Item.objects.create(
                title=f"{item_name}{i}",
                value=randint(1, 50000),
                rarity=randint(1, 5),
                author=cls.user,
            )

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
    URL_NAME = "library:item-list"

    @classmethod
    def setUpTestData(cls):
        # Create user
        cls.user = User.objects.create_user(username="testuser", password="testing321")

        item_name = "Item"

        # Create enough items for one page with random values
        for i in range(ITEMS_PER_PAGE):
            Item.objects.create(
                title=f"{item_name}{i}",
                value=randint(1, 50000),
                rarity=randint(1, 5),
                author=cls.user,
            )

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


class ItemLibraryDeleteViewTest(TestCase):
    URL_NAME = "library:item-delete"

    @classmethod
    def setUpTestData(cls):
        cls.first_user = User.objects.create_user(
            username="firstuser", password="testing321"
        )
        cls.second_user = User.objects.create_user(
            username="seconduser", password="testing123"
        )

        cls.first_item = Item.objects.create(
            title="FirstItem",
            author=cls.first_user,
        )
        cls.second_item = Item.objects.create(
            title="SecondItem",
            author=cls.second_user,
        )

    def setUp(self):
        self.client = Client()

    def test_user_can_delete_item(self):
        self.login_successful = self.client.login(
            username="firstuser", password="testing321"
        )

        # Simulate logged in user deleting a view
        self.client.post(reverse(self.URL_NAME, args=[self.first_item.id]))

        self.assertEqual(Item.objects.filter(title=self.first_item.title).count(), 0)

    def test_anonymous_user_can_not_delete_item(self):
        # Simulate anonymous user deleting a view
        self.client.post(reverse(self.URL_NAME, args=[self.second_item.id]))

        self.assertNotEqual(
            Item.objects.filter(title=self.second_item.title).count(), 0
        )

    def test_first_user_can_not_delete_item_second_user_item(self):
        self.client.login(username="firstuser", password="testing321")

        # Simulate anonymous user trying delete a view
        self.client.post(reverse(self.URL_NAME, args=[self.second_item.id]))

        self.assertNotEqual(
            Item.objects.filter(title=self.second_item.title).count(), 0
        )


class ItemLibraryUpdateViewTest(TestCase):
    URL_NAME = "library:item-update"

    @classmethod
    def setUpTestData(cls):
        cls.first_user = User.objects.create_user(
            username="firstuser", password="testing321"
        )
        cls.second_user = User.objects.create_user(
            username="seconduser", password="testing123"
        )

    def setUp(self):
        self.client = Client()

        self.item_for_editing = Item.objects.create(
            title="EditableItem",
            description="Edit This.",
            value=1000,
            rarity=4,
            author=self.first_user,
        )

    def test_user_can_edit_item(self):
        self.client.login(username="firstuser", password="testing321")
        form_data = {"title": "Lance"}

        # Simulate logged in user editing a view
        res = self.client.post(
            reverse(self.URL_NAME, args=[self.item_for_editing.id]), data=form_data
        )
        item = Item.objects.get(author=self.first_user)

        self.assertEqual(res.status_code, 302)
        self.assertEqual(item.title, form_data["title"])

    # other user changing other users item
    def test_other_user_can_not_change_item(self):
        self.client.login(username="seconduser", password="testing123")
        form_data = {"title": "Morningstar"}

        # Simulate logged in user trying to edit item that belong to different user
        res = self.client.post(
            reverse(self.URL_NAME, args=[self.item_for_editing.id]), data=form_data
        )
        item = Item.objects.get(author=self.first_user)

        # User should not be able to access other user items
        self.assertEqual(res.status_code, 403)
        self.assertNotEqual(item.title, form_data["title"])

    def test_form_invalid(self):
        form_data = {"title": ""}

        # Simulate logged in user trying to submit invalid title
        res = self.client.post(
            reverse(self.URL_NAME, args=[self.item_for_editing.id]), data=form_data
        )
        item = Item.objects.get(author=self.first_user)

        # User should be redirected after submitting invalid form
        self.assertEqual(res.status_code, 302)
        self.assertNotEqual(item.title, form_data["title"])
