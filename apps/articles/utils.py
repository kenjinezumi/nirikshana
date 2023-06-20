from langdetect import detect, detect_langs
from django.core.exceptions import ValidationError
import validators

def detect_language(content: str, method: str = "single") -> str:
    if method.lower() != "single":
        result = detect_langs(content)
    else:
        result = detect(content)
    return result

def validate_url(url: str) -> bool:
    if not validators.url(url):
        raise ValidationError(f"The URL {url} is not correct")
    else:
        return True

