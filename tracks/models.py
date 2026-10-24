from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.functions import Lower
from django.utils.text import slugify

from core.validators import validate_year


# Create your models here.
class Track(models.Model):
    class StyleChoices(models.TextChoices):
        BOOM_BAP = "boom_bap", "Boom Bap"
        TRAP = "trap", "Trap"
        DRILL = "drill", "Drill"
        G_FUNK = "g_funk", "G-Funk"
        CONSCIOUS = "conscious", "Conscious"
        JAZZ_RAP = "jazz_rap", "Jazz Rap"
        CLOUD_RAP = "cloud_rap", "Cloud Rap"
        ALTERNATIVE = "alternative", "Alternative"
        OTHER = "other", "Other"

    title = models.CharField(
        max_length=50,
    )
    performer = models.CharField(
        max_length=50,
    )
    release_year = models.IntegerField(
        validators=[
            validate_year,
        ],
    )
    release_date = models.DateField(
        blank=True,
        null=True,
    )
    bpm = models.IntegerField(
        validators=[
            MinValueValidator(40),
            MaxValueValidator(225),
        ],
    )
    style = models.CharField(
        max_length=20,
        choices=StyleChoices.choices,
        default=StyleChoices.OTHER,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    producer = models.ForeignKey(
        "producers.Producer",
        on_delete=models.PROTECT,
        related_name="tracks",
    )

    samples = models.ManyToManyField(
        "records.SourceRecord",
        related_name="tracks",
        blank=True,
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
        editable=False,
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.title}-{self.performer}")
        super().save(*args, **kwargs)

    def clean(self) -> None:
        super().clean()
        if self.release_date:
            if self.release_year != self.release_date.year:
                raise ValidationError("Release year must match the release date.")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('title'),
                Lower('performer'),
                name="unique_track_per_performer",
                violation_error_message="A track with this title and performer already exists.",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.title} by {self.performer}"