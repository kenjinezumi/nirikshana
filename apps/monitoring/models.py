from django.contrib.gis.db import models
from apps.utils import generate_latitude_longitude, detect_language
import logging
logger = logging.getLogger("nirikshana")

# Set the logging level
logger.setLevel(logging.DEBUG)

class Events(models.Model):
    """
    Model representing events.

    Fields:
        title (CharField): The title of the event.
        postal_code (CharField): The postal code of the event location.
        city (CharField): The city of the event location.
        address (CharField): The address of the event location.
        longitude (CharField): The longitude coordinate of the event location.
        latitude (CharField): The latitude coordinate of the event location.
        content (TextField): The content or description of the event.
        email_address (CharField): The email address associated with the event.
        phone_number (CharField): The phone number associated with the event.
        timestamp (DateTimeField): The timestamp when the event was created.
        validation_stage (CharField): The validation stage of the event.
        point (PointField): The geographic point representing the event location.

    Methods:
        __str__(): Returns a string representation of the event.
        article_language: Property that detects the language of the event content.
        generate_latitude_longitude(): Generates the latitude and longitude coordinates for the event location.
    """

    VALIDATION_STAGES = [
        ('Approved', 'Approved'),
        ('To be reviewed', 'To be reviewed'),
        ('Rejected', 'Rejected'),
    ]
    title = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    longitude = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    email_address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    validation_stage = models.CharField(max_length=50, choices=VALIDATION_STAGES)
    point = models.PointField(null=True, blank=True)

    def __str__(self):
        """
        Returns a string representation of the event.

        Returns:
            str: The title of the event.
        """
        return self.title

    @property
    def article_language(self):
        """
        Property that detects the language of the event content.

        Returns:
            str: The detected language of the event content.
        """
        return detect_language(self.content)

    def generate_latitude_longitude(self) -> None:
        """
        Generates the latitude and longitude coordinates for the event location.

        Returns:
            None
        """
        latitude, longitude = generate_latitude_longitude(self.address)
        if latitude is not None and longitude is not None:
            self.latitude = str(latitude)
            self.longitude = str(longitude)
            self.point = models.Point(longitude, latitude)
        else:
            self.latitude = None
            self.longitude = None
            self.point = None
