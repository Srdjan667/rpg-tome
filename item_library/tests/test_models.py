from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from item_library.models import Item, Spell


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


class SpellModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="testuser")
        cls.spell = Spell.objects.create(
            title="Levitate", school=7, level=4, author=cls.user
        )

    def test_spell_valid(self):
        db_entry = Spell.objects.get(title="Levitate")

        self.assertEqual(db_entry.title, "Levitate")
        # full_clean() returns None if no exceptions are raised
        self.assertIsNone(self.spell.full_clean())

    def test_invalid_spell_school(self):
        school_below_minimum_value = Spell(
            title="Minor Ilusion", school=-1, author=self.user
        )
        school_above_maximum_value = Spell(
            title="Invisibility", school=9, author=self.user
        )
        self.assertRaises(ValidationError, school_below_minimum_value.full_clean)
        self.assertRaises(ValidationError, school_above_maximum_value.full_clean)

    def test_invalid_spell_level(self):
        level_below_minimum_value = Spell(title="Fog", level=-1, author=self.user)
        level_above_maximum_value = Spell(
            title="Arcane Gate", level=10, author=self.user
        )

        self.assertRaises(ValidationError, level_below_minimum_value.full_clean)
        self.assertRaises(ValidationError, level_above_maximum_value.full_clean)

    def test_school_and_value_displayed_correctly(self):
        self.assertEqual(self.spell.get_school_display(), "Necromancy")
        self.assertEqual(self.spell.get_level_display(), "4th")
