from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from core.validators import validate_year


# Create your models here.
class SourceRecord(models.Model):
    class GenreChoices(models.TextChoices):
        SOUL = "soul", "Soul"
        JAZZ = "jazz", "Jazz"
        FUNK = "funk", "Funk"
        DISCO = "disco", "Disco"
        RNB = "rnb", "R&B"
        ELECTRONIC = "electronic", "Electronic"
        POP = "pop", "Pop"
        ROCK = "rock", "Rock"
        REGGAE = "reggae", "Reggae"
        AFROBEAT = "afrobeat", "Afrobeat"
        LATIN = "latin", "Latin"
        OTHER = "other", "Other"

    title = models.CharField(
        max_length=50,
    )
    original_artist = models.CharField(
        max_length=45,
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
    genre = models.CharField(
        max_length=20,
        choices=GenreChoices.choices,
        default=GenreChoices.OTHER,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    slug = models.SlugField(
        max_length=100,
        unique=True,
        editable=False,
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.title}-{self.original_artist}")
        super().save(*args, **kwargs)

    def clean(self) -> None:
        super().clean()
        if self.release_date:
            if self.release_year != self.release_date.year:
                raise ValidationError("Release year must match the release date.")

    def __str__(self) -> str:
        return f"{self.title} by {self.original_artist}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'original_artist'],
                name='unique_title_per_original_artist',
                violation_error_message="A record with this title and original artist already exists.",
            ),
        ]