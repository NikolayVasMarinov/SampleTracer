from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Min
from django.db.models.functions import Lower

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
    )
    country = models.CharField(
        choices=CountryChoices.choices,
        max_length=2,
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
            raise ValidationError({
                "region": (
                    "A region can only be selected for producers "
                    "from the USA."
                ),
            })

        if self.country == self.CountryChoices.USA and not self.region:
            raise ValidationError({
                "region": (
                    "Choose region for producers from the USA."
                ),
            })

        if self.pk is not None:
            earliest_track_year = self.tracks.aggregate(
                min_release_year=Min("release_year")
            )["min_release_year"]

            if (
                self.active_since is not None
                and earliest_track_year is not None
                and self.active_since > earliest_track_year
            ):
                raise ValidationError({
                    "active_since": (
                        f"Cannot be later than this producer's earliest "
                        f"track release year ({earliest_track_year})."
                    ),
                })

    def __str__(self) -> str:
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="unique_producer_name",
                violation_error_message="Producer name must be unique",
            ),
        ]
        ordering = ["name"]

