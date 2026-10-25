from django import forms

from core.utils import parse_length, format_length
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