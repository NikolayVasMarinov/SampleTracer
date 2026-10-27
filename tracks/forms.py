from django import forms

from core.utils import parse_length, format_length
from core.validators import validate_year
from producers.models import Producer
from records.models import SourceRecord
from .models import Track
from datetime import datetime


class TrackForm(forms.ModelForm):
    length = forms.CharField(
        max_length=5,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "3:30"}),
        label="Length",
        help_text="Track length in m:ss format",
        error_messages={
            "required": "Track length is required",
            "max_length": "Track length must be no longer than 5 characters",
        },
    )

    class Meta:
        model = Track
        exclude = ["slug", "created_at", "updated_at"]
        widgets = {
            "release_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "title": forms.TextInput(attrs={"placeholder": "Track title"}),
            "performer": forms.TextInput(attrs={"placeholder": "Performer name"}),
            "release_year": forms.NumberInput(attrs={"placeholder": "1999", "min": 1900, "max": datetime.now().year}),
            "bpm": forms.NumberInput(attrs={"placeholder": "120", "min": 40, "max": 225}),
        }
        labels = {
            "release_year": "Release Year",
            "release_date": "Release Date (Optional)",
            "samples": "Samples Used",
            "musical_key": "Musical Key (Optional)",
            "bpm": "BPM",
        }
        help_texts = {
            "release_year": "The year the track was released",
            "release_date": "The full date the track was released",
            "samples": "Select all samples used in the track (hold Ctrl or Cmd to select multiple)",
            "performer": "In case of multiple performers, separate names with commas",
            "musical_key": "Leave empty if unknown",
        }
        error_messages = {
            "title": {
                "required": "Track title is required",
                "max_length": "Track title must be no longer than 50 characters"
            },
            "performer": {
                "required": "Performer name is required",
                "max_length": "Performer name must be no longer than 50 characters"
            },
            "release_year": {
                "required": "Release year is required",
            },
            "release_date": {"invalid": "Invalid date"},
            "bpm": {
                "required": "Track BPM is required",
                "min_value": "Track BPM must be in a sensible range (40-225)",
                "max_value": "Track BPM must be in a sensible range (40-225)",
            },
            "style": {
                "required": "Track style is required",
                "invalid_choice": "Invalid track style",
            },
            "musical_key": {"invalid_choice": "Invalid musical key"},
            "producer": {
                "required": "Producer of the track is required",
                "invalid_choice": "Invalid producer",
            },
        }

    def clean_length(self):
        length_in_seconds = parse_length(self.cleaned_data["length"])
        return length_in_seconds

    def clean(self):
        cleaned_data = super().clean()
        release_year = cleaned_data.get("release_year")
        release_date = cleaned_data.get("release_date")
        samples = cleaned_data.get("samples")
        producer = cleaned_data.get("producer")

        if (
            producer
            and release_year is not None
            and producer.active_since is not None
            and producer.active_since > release_year
        ):
            self.add_error(
                "release_year",
                f"{producer.name} became active in {producer.active_since}, "
                f"so the track cannot have been released before that year.",
            )

        problem_samples = []

        if samples:
            for sample in samples:
                if release_year and sample.release_year and release_year < sample.release_year:
                    problem_samples.append(sample)

                elif release_date and sample.release_date and release_date < sample.release_date:
                    problem_samples.append(sample)

            if problem_samples:
                error = f"{', '.join([s.title + ' (' + str(s.release_year) + ')' for s in problem_samples])} "
                if len(problem_samples) == 1:
                    error += f"was released after this track"
                else:
                    error += f"were released after this track"

                self.add_error(
                    "samples",
                    error
                )

        return cleaned_data

class TrackEditForm(TrackForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["producer"].disabled = True
        if self.instance.pk:
            self.initial["length"] = format_length(self.instance.length)

class TrackFilterForm(forms.Form):
    title = forms.CharField(
        required=False,
        max_length=50,
        label="Track title",
        widget=forms.TextInput(
            attrs={"placeholder": "Search track title"}
        ),
        error_messages={
            "max_length": "Track title must not exceed 50 characters.",
        },
    )

    performer = forms.CharField(
        required=False,
        max_length=50,
        label="Performer",
        widget=forms.TextInput(
            attrs={"placeholder": "Search performer"}
        ),
        error_messages={
            "max_length": "Performer name must not exceed 50 characters.",
        },
    )

    style = forms.ChoiceField(
        required=False,
        label="Style",
        choices=[("", "All styles")] + list(Track.StyleChoices.choices),
        error_messages={
            "invalid_choice": "Select a valid track style.",
        },
    )

    release_year_from = forms.IntegerField(
        required=False,
        label="Released from",
        validators=[validate_year],
        widget=forms.NumberInput(
            attrs={
                "placeholder": "e.g. 1999",
                "min": 1900,
                "max": datetime.now().year,
            }
        ),
        help_text="Earliest release year.",
        error_messages={
            "invalid": "Enter a valid whole-number starting year.",
        },
    )

    release_year_to = forms.IntegerField(
        required=False,
        label="Released to",
        validators=[validate_year],
        widget=forms.NumberInput(
            attrs={
                "placeholder": "e.g. 2020",
                "min": 1900,
                "max": datetime.now().year,
            }
        ),
        help_text="Latest release year.",
        error_messages={
            "invalid": "Enter a valid whole-number ending year.",
        },
    )

    producer = forms.ModelChoiceField(
        required=False,
        label="Producer",
        queryset=Producer.objects.all(),
        empty_label="All producers",
        error_messages={
            "invalid_choice": "Select a valid producer.",
        },
    )

    sampled_record = forms.ModelChoiceField(
        required=False,
        label="Sampled record",
        queryset=SourceRecord.objects.all(),
        empty_label="Any record",
        error_messages={
            "invalid_choice": "Select a valid sampled record.",
        },
    )

    sort = forms.ChoiceField(
        required=False,
        label="Sort by",
        choices=[
            ("", "Default order"),
            ("newest", "Newest first"),
            ("oldest", "Oldest first"),
            ("title", "Title A–Z"),
            ("bpm_low", "BPM, low to high"),
            ("bpm_high", "BPM, high to low"),
            ("longest", "Longest first"),
            ("shortest", "Shortest first"),
        ],
        error_messages={
            "invalid_choice": "Select a valid sorting option.",
        },
    )

    def clean(self):
        cleaned_data = super().clean()

        year_from = cleaned_data.get("release_year_from")
        year_to = cleaned_data.get("release_year_to")

        if (
            year_from is not None
            and year_to is not None
            and year_from > year_to
        ):
            self.add_error(
                "release_year_to",
                "The ending year must be greater than or equal to the starting year.",
            )

        return cleaned_data