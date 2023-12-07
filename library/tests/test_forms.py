from django.test import TestCase

from library import forms as library_forms

RARITIES = ["Common", "Uncommon", "Rare", "Very Rare", "Legendary", "Artifact"]


class ItemsFormTest(TestCase):
    def test_empty_form(self):
        form = library_forms.ItemsForm()

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
        form = library_forms.ItemsForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_form_title_invalid(self):
        form_data = {"title": ""}
        form = library_forms.ItemsForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_form_description_invalid(self):
        form_data = {"description": None}
        form = library_forms.ItemsForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_form_value_invalid(self):
        form_data = {"value": -1}
        form = library_forms.ItemsForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_form_rarity_invalid(self):
        form_data = {"rarity": 7}
        form = library_forms.ItemsForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_default_value(self):
        form_data = {"title": "Anduril"}
        form = library_forms.ItemsForm(data=form_data)

        form.is_valid()

        # Make sure value is 0 when nothing is provided
        self.assertEqual(form.cleaned_data["value"], 0)


class ItemFilterFormTest(TestCase):
    def test_empty_form_is_valid(self):
        form_data = {}
        form = library_forms.ItemFilterForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_form_is_valid(self):
        form_data = {
            "title": "sword",
            "min_value": 0,
            "max_value": 1000,
            "rarity": [1, 4, 5],
        }
        form = library_forms.ItemFilterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_min_value_is_zero(self):
        form_data = {
            "min_value": 0,
        }
        form = library_forms.ItemFilterForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {
            "min_value": 1000,
        }
        form = library_forms.ItemFilterForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {
            "min_value": -10,
        }
        form = library_forms.ItemFilterForm(data=form_data)
        self.assertFalse(form.is_valid())


class SpellsFormTest(TestCase):
    def test_form_is_valid(self):
        form_data = {
            "title": "Arcane Gate",
            "description": "Open gate to another world",
            "school": 4,
            "level": 4,
        }
        form = library_forms.SpellsForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            # The title must be present if the form is to be valid
            "description": "Open gate to another world",
            "school": 4,
            "level": 4,
        }
        form = library_forms.SpellsForm(data=form_data)

        self.assertFalse(form.is_valid())


class SpellFilterFormTest(TestCase):
    def test_empty_form_is_valid(self):
        form_data = {}
        form = library_forms.SpellFilterForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_form_is_valid(self):
        form_data = {
            "title": "sword",
            "school": [1, 4, 7],
            "level": [7, 4, 1],
        }
        form = library_forms.SpellFilterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_only_accepts_list_of_integers(self):
        form_data = {
            "school": [1, 4, 7],
        }
        form = library_forms.SpellFilterForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {
            "school": ["elementary", 4, 7],
        }
        form = library_forms.SpellFilterForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            "school": [5.56, 4, 7],
        }
        form = library_forms.SpellFilterForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            "school": 7,
        }
        form = library_forms.SpellFilterForm(data=form_data)
        self.assertFalse(form.is_valid())


class SpellSortFormTest(TestCase):
    def test_empty_form_is_valid(self):
        form_data = {}
        form = library_forms.SpellSortForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_form_is_valid(self):
        form_data = {
            "sort_direction": "",
            "sort_criteria": "",
        }
        form = library_forms.SpellSortForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_only_accepts_valid_direction(self):
        form_data = {"sort_direction": "asc"}
        form = library_forms.SpellSortForm(data=form_data)

        self.assertTrue(form.is_valid())

        form_data = {"sort_direction": "desc"}
        form = library_forms.SpellSortForm(data=form_data)

        self.assertTrue(form.is_valid())

        form_data = {"sort_direction": "dummy_direction"}
        form = library_forms.SpellSortForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["sort_direction"][0],
            "Select a valid choice. dummy_direction is not one of the available choices.",
        )
