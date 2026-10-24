from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from core.validators import validate_year

# Create your models here.
class Producer(models.Model):
    class CountryChoices(models.TextChoices):
        USA = "US", "USA"
        UK = "UK", "United Kingdom"
        FRANCE = "FR", "France"
        BRAZIL = "BR", "Brazil"
        NIGERIA = "NG", "Nigeria"
        OTHER = "OT", "Other"

    class RegionChoices(models.TextChoices):
        WEST_COAST = "WC", "West Coast"
        EAST_COAST = "EC", "East Coast"
        MIDWEST = "MW", "Midwest"
        SOUTH = "SO", "South"
        OTHER = "OT", "Other"

    name = models.CharField(
        max_length=40,
        unique=True,
        validators=[
            MinLengthValidator(2),
        ],
    )
    country = models.CharField(
        choices=CountryChoices.choices,
        max_length=2,
        validators=[
            MinLengthValidator(2),
        ],
        default=CountryChoices.OTHER,
    )
    region = models.CharField(
        choices=RegionChoices.choices,
        max_length=2,
        blank=True,
    )
    active_since = models.IntegerField(
        validators=[
            validate_year,
        ],
    )
    bio = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self) -> None:
        super().clean()
        if self.region and self.country != self.CountryChoices.USA:
            raise ValidationError("Region can only be set for USA producers")

    def __str__(self) -> str:
        return self.name

