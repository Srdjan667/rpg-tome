from django import forms
from django.core.validators import MinValueValidator
from django.forms import ModelForm

from .models import Item


class CreateItemForm(ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter title here", "autofocus": True}
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter description here"})
    )

    value = forms.IntegerField(
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={"placeholder": "Enter value here"}),
    )

    rarity = forms.IntegerField(
        widget=forms.Select(
            choices=Item.RARITIES, attrs={"placeholder": "Select rarity level"}
        ),
        required=True,
    )

    class Meta:
        model = Item
        fields = ["title", "description", "value", "rarity"]
