from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.functions import Lower
from django.utils.text import slugify

from core.constants import MAX_LENGTH_SECONDS
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

    class MusicalKeyChoices(models.TextChoices):
        C_MINOR = "C_MIN", "C Minor"
        CS_MINOR = "CS_MIN", "C# Minor / Db Minor"
        D_MINOR = "D_MIN", "D Minor"
        DS_MINOR = "DS_MIN", "D# Minor / Eb Minor"
        F_MINOR = "F_MIN", "F Minor"
        FS_MINOR = "FS_MIN", "F# Minor / Gb Minor"
        A_MINOR = "A_MIN", "A Minor"
        E_MINOR = "E_MIN", "E Minor"
        G_MINOR = "G_MIN", "G Minor"
        GS_MINOR = "GS_MIN", "G# Minor / Ab Minor"
        B_MINOR = "B_MIN", "B Minor"
        AS_MINOR = "AS_MIN", "A# Minor / Bb Minor"
        C_MAJOR = "C_MAJ", "C Major"
        CS_MAJOR = "CS_MAJ", "C# Major / Db Major"
        D_MAJOR = "D_MAJ", "D Major"
        DS_MAJOR = "DS_MAJ", "D# Major / Eb Major"
        E_MAJOR = "E_MAJ", "E Major"
        F_MAJOR = "F_MAJ", "F Major"
        FS_MAJOR = "FS_MAJ", "F# Major / Gb Major"
        G_MAJOR = "G_MAJ", "G Major"
        GS_MAJOR = "GS_MAJ", "G# Major / Ab Major"
        A_MAJOR = "A_MAJ", "A Major"
        AS_MAJOR = "AS_MAJ", "A# Major / Bb Major"
        B_MAJOR = "B_MAJ", "B Major"

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
        error_messages={
            "min_value": "BPM must be in a sensible range.",
            "max_value": "BPM must be in a sensible range.",
        },
    )
    style = models.CharField(
        max_length=20,
        choices=StyleChoices.choices,
        default=StyleChoices.OTHER,
    )
    length = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(MAX_LENGTH_SECONDS),
        ],
        error_messages={
            "min_value": "Track must be at least 1 second long.",
            "max_value": f"Track cannot exceed {MAX_LENGTH_SECONDS // 60} minutes in length.",
        },
    )
    musical_key = models.CharField(
        max_length=10,
        choices=MusicalKeyChoices.choices,
        blank=True,
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

    @property
    def sample_count(self) -> int:
        return self.samples.count()

    @property
    def musical_key_root(self) -> str:
        """Return the root note of the musical key."""
        return self.musical_key.split("_")[0].replace("S", "#")


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
        ordering = ["release_year", "title", "pk"]

    def __str__(self) -> str:
        return f"{self.title} by {self.performer}"