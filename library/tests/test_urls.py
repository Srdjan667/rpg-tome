from django.test import SimpleTestCase
from django.urls import resolve, reverse

from library import views


class TestItemLibraryUrls(SimpleTestCase):
    def test_item_list_is_resolved(self):
        url = reverse("library:item-list")
        self.assertEquals(resolve(url).func, views.item_list)

    def test_item_create_is_resolved(self):
        url = reverse("library:item-create")
        self.assertEquals(resolve(url).func, views.new_item)

    def test_item_detail_is_resolved(self):
        url = reverse("library:item-detail", args=[1])
        self.assertEquals(resolve(url).func.view_class, views.ItemDetailView)

    def test_item_update_is_resolved(self):
        url = reverse("library:item-update", args=[1])
        self.assertEquals(resolve(url).func.view_class, views.ItemUpdateView)

    def test_item_delete_is_resolved(self):
        url = reverse("library:item-delete", args=[1])
        self.assertEquals(resolve(url).func.view_class, views.ItemDeleteView)


class TestSpellUrls(SimpleTestCase):
    def test_spell_list_is_resolved(self):
        url = reverse("library:spell-list")
        self.assertEquals(resolve(url).func, views.spell_list)

    def test_spell_detail_is_resolved(self):
        url = reverse("library:spell-detail", args=[1])
        self.assertEquals(resolve(url).func.view_class, views.SpellDetailView)

    def test_spell_update_is_resolved(self):
        url = reverse("library:spell-update", args=[1])
        self.assertEquals(resolve(url).func.view_class, views.SpellUpdateView)

    def test_spell_delete_is_resolved(self):
        url = reverse("library:spell-delete", args=[1])
        self.assertEquals(resolve(url).func.view_class, views.SpellDeleteView)
