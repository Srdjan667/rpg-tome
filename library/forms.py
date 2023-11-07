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
