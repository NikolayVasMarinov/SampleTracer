from datetime import datetime
from django.core.exceptions import ValidationError


def validate_year(year: int):
    if year < 1900 or year > datetime.now().year:
        raise ValidationError(f"Year must be between 1900 and {datetime.now().year}")