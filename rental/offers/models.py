from django.conf import settings
from django.db import models


class Offer(models.Model):
    class Size(models.TextChoices):
        STUDIO = "ST", "Studio"
        ONE_BEDROOM = "1BR", "1 bedroom"
        TWO_BEDROOMS = "2BR", "2 bedrooms"
        THREE_BEDROOMS = "3BR", "3 bedrooms"
        MORE_BEDROOMS = "MBR", "3+ bedrooms"

    class PropertyType(models.TextChoices):
        HOUSE = "H", "house"
        APARTMENT = "APT", "apartment"

    created = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=100, blank=True, default="")
    size = models.CharField(choices=Size.choices, default=Size.ONE_BEDROOM, max_length=100)
    property_type = models.CharField(
        choices=PropertyType.choices, default=PropertyType.APARTMENT, max_length=100
    )
    price = models.PositiveIntegerField(default=0)
    sharing = models.BooleanField(default=False)
    text = models.TextField(default="")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="offers",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["created"]

    def __str__(self) -> str:
        return f"{self.address} - {self.get_property_type_display()}"
