from django import forms

from core.utils import parse_length
from .models import SourceRecord

from datetime import datetime


class SourceRecordForm(forms.ModelForm):
    length = forms.CharField(
        max_length=5,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "3:30"}),
        label="Length",
        help_text="Record length in m:ss format",
        error_messages={
            "required": "Record length is required",
            "max_length": "Record length must be no longer than 5 characters",
        },
    )

    class Meta:
        model = SourceRecord
        fields = ["title", "original_artist", "release_year", "release_date", "genre", "length"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Record title"}),
            "original_artist": forms.TextInput(attrs={"placeholder": "Original artist"}),
            "release_year": forms.NumberInput(attrs={"placeholder": "1999", "min": 1900, "max": datetime.now().year}),
            "release_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }
        labels = {
            "release_year": "Release Year",
            "release_date": "Release Date (Optional)",
            "original_artist": "Artist",
        }
        help_texts = {
            "release_year": "The year the record was released",
            "release_date": "The full date the record was released",
            "original_artist": "In case of multiple performers, separate names with commas",
        }
        error_messages = {
            "title": {
                "required": "Record title is required",
                "max_length": "Record title must be no longer than 50 characters"
            },
            "original_artist": {
                "required": "Artist name is required",
                "max_length": "Artist name must be no longer than 45 characters"
            },
            "release_year": {
                "required": "Release year is required",
            },
            "release_date": {"invalid": "Invalid date"},
            "genre": {"invalid_choice": "Invalid record genre"},
        }

    def clean_length(self):
        length_in_seconds = parse_length(self.cleaned_data["length"])
        return length_in_seconds

