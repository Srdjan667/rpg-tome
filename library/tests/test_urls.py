from django.test import SimpleTestCase
from django.urls import resolve, reverse

from library.views import (
    ItemDeleteView,
    ItemDetailView,
    ItemUpdateView,
    item_list,
    new_item,
)


class TestItemLibraryUrls(SimpleTestCase):
    def test_index_is_resolved(self):
        url = reverse("library:item-list")
        self.assertEquals(resolve(url).func, item_list)

    def test_item_create_is_resolved(self):
        url = reverse("library:item-create")
        self.assertEquals(resolve(url).func, new_item)

    def test_item_detail_is_resolved(self):
        url = reverse("library:item-detail", args=[1])
        self.assertEquals(resolve(url).func.view_class, ItemDetailView)

    def test_item_update_is_resolved(self):
        url = reverse("library:item-update", args=[1])
        self.assertEquals(resolve(url).func.view_class, ItemUpdateView)

    def test_item_delete_is_resolved(self):
        url = reverse("library:item-delete", args=[1])
        self.assertEquals(resolve(url).func.view_class, ItemDeleteView)
