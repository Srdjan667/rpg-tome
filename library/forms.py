from django import forms
from django.core.validators import MinValueValidator
from django.forms import ModelForm

from library.models import Item, Spell


class ItemsForm(ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter title here", "autofocus": True}
        ),
        required=True,
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter description here"}),
        required=False,
    )

    value = forms.IntegerField(
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={"placeholder": "Enter value here"}),
        required=False,
    )

    rarity = forms.IntegerField(
        widget=forms.Select(
            choices=Item.RARITIES, attrs={"placeholder": "Select rarity level"}
        ),
        required=False,
    )

    class Meta:
        model = Item
        fields = ["title", "description", "value", "rarity"]

    def clean_value(self):
        data = self.cleaned_data["value"]
        if data is None:
            return 0
        return data


class ItemFilterForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter title here", "class": "form-control"},
        ),
        required=False,
        initial="",
    )

    min_value = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"placeholder": "Min value", "class": "form-control"},
        ),
        min_value=0,
        required=False,
    )

    max_value = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"placeholder": "Max value", "class": "form-control"},
        ),
        required=False,
    )

    rarity = forms.TypedMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "form-check-input"},
        ),
        choices=Item.RARITIES,
        coerce=int,
        required=False,
    )


class ItemSortForm(forms.Form):
    sort_criteria = forms.ChoiceField(
        choices=Item.SORT_CRITERIA,
        required=False,
    )

    sort_direction = forms.ChoiceField(
        choices=Item.SORT_DIRECTION,
        required=False,
    )

    def clean_sort_criteria(self):
        data = self.cleaned_data["sort_criteria"]
        for criteria in Item.SORT_CRITERIA:
            if data == criteria[0]:
                return data
        return "date_created"

    def clean_sort_direction(self):
        data = self.cleaned_data["sort_direction"]
        for direction in Item.SORT_DIRECTION:
            if data == direction[0]:
                return data
        return "desc"


class SpellsForm(ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter title here", "autofocus": True}
        ),
        required=True,
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter description here"}),
        required=False,
    )

    school = forms.IntegerField(
        widget=forms.Select(
            choices=Spell.SCHOOLS_OF_MAGIC,
            attrs={"placeholder": "Select school of magic"},
        ),
        required=False,
    )

    level = forms.IntegerField(
        widget=forms.Select(
            choices=Spell.SPELL_LEVELS,
            attrs={"placeholder": "Select level of your spell"},
        ),
        required=False,
    )

    class Meta:
        model = Spell
        fields = ["title", "description", "school", "level"]

    def clean_school(self):
        data = self.cleaned_data["school"]
        if data is None:
            return 0
        return data

    def clean_level(self):
        data = self.cleaned_data["level"]
        if data is None:
            return 0
        return data


class SpellFilterForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter title here", "class": "form-control"}
        ),
        required=False,
    )

    school = forms.TypedMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "form-check-input"},
        ),
        choices=Spell.SCHOOLS_OF_MAGIC,
        coerce=int,
        required=False,
    )

    level = forms.TypedMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "form-check-input"},
        ),
        choices=Spell.SPELL_LEVELS,
        coerce=int,
        required=False,
    )


class SpellSortForm(forms.Form):
    sort_criteria = forms.ChoiceField(
        choices=Spell.SORT_CRITERIA,
        required=False,
    )

    sort_direction = forms.ChoiceField(
        choices=Spell.SORT_DIRECTION,
        required=False,
    )

    def clean_sort_criteria(self):
        data = self.cleaned_data["sort_criteria"]
        for criteria in Spell.SORT_CRITERIA:
            if data == criteria[0]:
                return data
        return "date_created"

    def clean_sort_direction(self):
        data = self.cleaned_data["sort_direction"]
        for direction in Spell.SORT_DIRECTION:
            if data == direction[0]:
                return data
        return "desc"
