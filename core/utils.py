from django.core.exceptions import ValidationError
import re

from core.constants import MAX_LENGTH_SECONDS

LENGTH_REGEX = re.compile("[0-9]{1,2}:[0-5][0-9]")

def validate_length_format(length):
    if not LENGTH_REGEX.fullmatch(length):
        raise ValidationError("Length must be in m:ss format, for example 3:45")

def length_to_seconds(length):
    return int(length.split(":")[0]) * 60 + int(length.split(":")[1])

def format_length(length):
    if length is None or length == "":
        return ""
    return f"{length // 60}:{length % 60:02d}"

def parse_length(length):
    validate_length_format(length)

    length_in_seconds = length_to_seconds(length)

    if length_in_seconds < 1:
        raise ValidationError("Length must be longer than 0 seconds")
    if length_in_seconds > MAX_LENGTH_SECONDS:
        raise ValidationError(f"Length must be no longer than {MAX_LENGTH_SECONDS // 60} minutes")
    return length_in_seconds
