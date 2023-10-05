from django.test import TestCase

from item_library.forms import ItemsForm, SpellsForm

RARITIES = ["Common", "Uncommon", "Rare", "Very Rare", "Legendary", "Artifact"]


class ItemsFormTest(TestCase):
    def test_empty_form(self):
        form = ItemsForm()

        self.assertInHTML(
            '<input type="text" name="title" placeholder="Enter title here" autofocus required id="id_title">',
            str(form),
        )
        self.assertInHTML(
            '<textarea name="description" cols="40" rows="10" placeholder="Enter description here" id="id_description">',
            str(form),
        )
        self.assertInHTML(
            '<input type="number" name="value" placeholder="Enter value here" id="id_value">',
            str(form),
        )

        # Check if all rarity options are present
        for i in range(len(RARITIES)):
            self.assertInHTML(
                f'<option value="{i+1}">{RARITIES[i]}</option>', str(form)
            )

    def test_form_is_valid(self):
        form_data = {
            "title": "Sword",
            "description": "Very sharp sword.",
            "value": 1000,
            "rarity": 6,
        }
        form = ItemsForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_form_title_invalid(self):
        form_data = {"title": ""}
        form = ItemsForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_form_description_invalid(self):
        form_data = {"description": None}
        form = ItemsForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_form_value_invalid(self):
        form_data = {"value": -1}
        form = ItemsForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_form_rarity_invalid(self):
        form_data = {"rarity": 7}
        form = ItemsForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_default_value(self):
        form_data = {"title": "Anduril"}
        form = ItemsForm(data=form_data)

        form.is_valid()

        # Make sure value is 0 when nothing is provided
        self.assertEqual(form.cleaned_data["value"], 0)


class SpellsFormTest(TestCase):
    def test_form_is_valid(self):
        form_data = {
            "title": "Arcane Gate",
            "description": "Open gate to another world",
            "school": 4,
            "level": 4,
        }
        form = SpellsForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            # The title must be present if the form is to be valid
            "description": "Open gate to another world",
            "school": 4,
            "level": 4,
        }
        form = SpellsForm(data=form_data)

        self.assertFalse(form.is_valid())
