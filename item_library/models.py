from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Item(models.Model):
    """
    By using integers to define choices, it's possible to enforce
    the set of allowed values in the database, and prevent invalid data
    from being inserted into the database.
    """

    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    VERY_RARE = 4
    LEGENDARY = 5

    RARITIES = (
        (1, "Common"),
        (2, "Uncommon"),
        (3, "Rare"),
        (4, "Very Rare"),
        (5, "Legendary"),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    value = models.PositiveIntegerField(default=0)
    rarity = models.PositiveSmallIntegerField(
        default=COMMON,
        choices=RARITIES,
        validators=[MaxValueValidator(len(RARITIES))],
    )

    date_created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("item_library:item-detail", args=[self.id])
