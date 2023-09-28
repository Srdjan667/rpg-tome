from django.test import TestCase

from item_library.forms import ItemsForm

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
