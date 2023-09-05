from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User

class Item(models.Model):
    """
    By using integers to define choices, it's possible to enforce 
    the set of allowed values in the database, and prevent invalid data 
    from being inserted into the database.
    """

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
                default=RARITIES[0][0], # This equals to common rarity
                choices=RARITIES, 
                validators=[MaxValueValidator(len(RARITIES))],
    )

    date_created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
