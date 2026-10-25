from django import forms
from .models import Producer


class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        fields = ["name", "country", "region", "active_since", "bio"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }
