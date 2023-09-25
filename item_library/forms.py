from django import forms
from django.core.validators import MinValueValidator
from django.forms import ModelForm

from .models import Item


class CreateItemForm(ModelForm):
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


class UpdateItemForm(ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter new title here", "autofocus": True}
        ),
        required=True,
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter new description here"}),
        required=False,
    )

    value = forms.IntegerField(
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={"placeholder": "Enter new value here"}),
        required=False,
    )

    rarity = forms.IntegerField(
        widget=forms.Select(
            choices=Item.RARITIES, attrs={"placeholder": "Select new rarity level"}
        ),
        required=False,
    )

    class Meta:
        model = Item
        fields = ["title", "description", "value", "rarity"]
