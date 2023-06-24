from langdetect import detect, detect_langs
from django.core.exceptions import ValidationError
import validators
from geopy.geocoders import Nominatim

def detect_language(content: str, method: str = "single") -> str:
    """
    Detects the language of the given content.

    Args:
        content (str): The content to detect the language from.
        method (str, optional): The method to use for language detection. Defaults to "single".

    Returns:
        str: The detected language.

    Raises:
        Nothing.

    Examples:
        >>> detect_language("Hello, world!")
        'en'
        >>> detect_language("Bonjour tout le monde!", method="detailed")
        [{'lang': 'fr', 'prob': 0.9999968944069294}]
    """
    if method.lower() != "single":
        result = detect_langs(content)
    else:
        result = detect(content)
    return result


def validate_url(url: str) -> bool:
    """
    Validates the format of a URL.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.

    Raises:
        ValidationError: If the URL is not in the correct format.

    Examples:
        >>> validate_url("http://example.com")
        True
        >>> validate_url("example.com")
        Raises ValidationError with message "The URL example.com is not correct"
    """
    if not validators.url(url):
        raise ValidationError(f"The URL {url} is not correct")
    return True


def generate_latitude_longitude(country: str, city: str = None,
                                postcode: str = None, street: str = None) -> tuple[float, float]:
    """
    Generates latitude and longitude coordinates for a given location.

    Args:
        country (str): The country name.
        city (str, optional): The city name. Defaults to None.
        postcode (str, optional): The postal code. Defaults to None.
        street (str, optional): The street name. Defaults to None.

    Returns:
        tuple[float, float]: The latitude and longitude coordinates.

    Raises:
        Nothing.

    Examples:
        >>> generate_latitude_longitude("United States")
        (37.09024, -95.712891)
        >>> generate_latitude_longitude("Canada", city="Toronto", postcode="M5V 2L7", street="123 Main St")
        (43.6444436, -79.3809625)
    """
    location_query = country
    if city:
        location_query += f", {city}"
    if postcode:
        location_query += f", {postcode}"
    if street:
        location_query += f", {street}"

    geolocator = Nominatim(user_agent='nirikshana')
    location = geolocator.geocode(location_query)

    if location is not None:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return None, None
