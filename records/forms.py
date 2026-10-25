from django import forms
from .models import SourceRecord


class SourceRecordForm(forms.ModelForm):
    class Meta:
        model = SourceRecord
        fields = ["title", "original_artist", "release_year", "release_date", "genre", "length"]
