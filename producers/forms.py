from django import forms
from .models import Producer

from datetime import datetime


class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        fields = ["name", "country", "region", "active_since", "bio"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Producer name"}),
            "bio": forms.Textarea(attrs={"rows": 4}),
            "active_since": forms.NumberInput(attrs={"placeholder": "1999", "min": 1900, "max": datetime.now().year}),
        }
        labels = {
            "name": "Producer's Name",
            "bio": "Producer's Bio (Optional)",
        }
        help_texts = {
            "country": "Country in which the producer is/was active",
            "region": "Available only if country is set to USA",
            "active_since": "Year producer started producing tracks",
        }
        error_messages = {
            "name": {
                "required": "Producer's name is required",
            },
            "country": {
                "required": "Country is required",
                "invalid_choice": "Invalid country"
            },
            "region": {
                "invalid_choice": "Invalid region"
            },
            "active_since": {
                "required": "Year is required",
            }
        }

    def clean(self):
        cleaned_data = super().clean()
        country = cleaned_data.get("country")
        region = cleaned_data.get("region")

        if region and country != Producer.CountryChoices.USA:
            self.add_error("region", "Region is only available if country is set to USA")

        if not region and country == Producer.CountryChoices.USA:
            self.add_error("region", "Region is required if country is set to USA")

        return cleaned_data