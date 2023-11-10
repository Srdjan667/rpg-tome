from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

ITEM_RARITY_MAP = {
    "common": 1,
    "uncommon": 2,
    "rare": 3,
    "very rare": 4,
    "legendary": 5,
    "artifact": 6,
}


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
    ARTIFACT = 6

    RARITIES = (
        (COMMON, "Common"),
        (UNCOMMON, "Uncommon"),
        (RARE, "Rare"),
        (VERY_RARE, "Very Rare"),
        (LEGENDARY, "Legendary"),
        (ARTIFACT, "Artifact"),
    )

    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    value = models.PositiveIntegerField(default=0, null=True)
    rarity = models.PositiveSmallIntegerField(
        default=COMMON,
        null=True,
        choices=RARITIES,
        validators=[MaxValueValidator(len(RARITIES))],
    )
    date_created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("library:item-detail", args=[self.id])

    def get_queryset(request, data):
        filters = {
            "title__icontains": data["title"],
            "date_created__lte": timezone.now(),
            "author": request.user,
        }

        # Also filter by these if present in form
        if data["min_value"]:
            filters.update({"value__gte": data["min_value"]})
        if data["max_value"]:
            filters.update({"value__lte": data["max_value"]})
        if data["rarity"]:
            filters.update({"rarity__in": data["rarity"]})

        # Filter items based on GET criteria
        items = Item.objects.filter(**filters)

        return items

    def sort_queryset(request, q):
        DIRECTION_MAPPING = {"ascending": "", "descending": "-"}

        # Gets order criteria from URL
        order = request.GET.get("order", "date_created")
        order_direction = request.GET.get("direction", "descending")

        order = order.replace(" ", "_")
        order_direction = DIRECTION_MAPPING[order_direction]

        return q.order_by(order_direction + order)


class Spell(models.Model):
    UNKNOWN = 0
    ABJURATION = 1
    CONJURATION = 2
    DIVINATION = 3
    ENCHANTMENT = 4
    EVOCATION = 5
    ILLUSION = 6
    NECROMANCY = 7
    TRANSMUTATION = 8

    SCHOOLS_OF_MAGIC = (
        (UNKNOWN, "Unknown"),
        (ABJURATION, "Abjuration"),
        (CONJURATION, "Conjuration"),
        (DIVINATION, "Divination"),
        (ENCHANTMENT, "Enchantment"),
        (EVOCATION, "Evocation"),
        (ILLUSION, "Illusion"),
        (NECROMANCY, "Necromancy"),
        (TRANSMUTATION, "Transmutation"),
    )

    SPELL_LEVELS = (
        (0, "Cantrip"),
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (5, "5th"),
        (6, "6th"),
        (7, "7th"),
        (8, "8th"),
        (9, "9th"),
    )

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    school = models.PositiveSmallIntegerField(
        choices=SCHOOLS_OF_MAGIC,
        default=UNKNOWN,
        validators=[MinValueValidator(0), MaxValueValidator(len(SCHOOLS_OF_MAGIC) - 1)],
    )
    level = models.PositiveSmallIntegerField(
        choices=SPELL_LEVELS,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(len(SPELL_LEVELS))],
    )
    date_created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("library:spell-detail", args=[self.id])

    def get_queryset(request, data):
        filters = {
            "title__icontains": data["title"],
            "date_created__lte": timezone.now(),
            "author": request.user,
        }

        # Also filter by these if present in form
        if data["school"]:
            filters.update({"school__in": data["school"]})
        if data["level"]:
            filters.update({"level__in": data["level"]})

        # Filter spells based on data
        spells = Spell.objects.filter(**filters)

        return spells
