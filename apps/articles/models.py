from django.db import models
import time
from apps.utils import detect_language, validate_url


class Articles(models.Model):
    """
    Model representing articles.

    Fields:
        source (CharField): The source of the article.
        url (CharField): The URL of the article.
        title (CharField): The title of the article.
        authors (CharField): The authors of the article.
        publication_date (CharField): The publication date of the article.
        article_content (TextField): The content of the article.
        timestamp (TextField): The timestamp when the article was created.
        validation_stage (CharField): The validation stage of the article.

    Methods:
        __str__(): Returns a string representation of the article.
        article_language: Property that detects the language of the article content.
    """

    VALIDATION_STAGES = (
        ('Approved', 'approved'),
        ('To be reviewed', 'to_be_reviewed'),
        ('Rejected', 'rejected'),
    )
    source = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True, validators=[validate_url])
    title = models.CharField(max_length=255, null=True, blank=True)
    authors = models.CharField(max_length=255, null=True, blank=True)
    publication_date = models.CharField(max_length=255, null=True, blank=True)
    article_content = models.TextField(null=True, blank=True)
    timestamp = models.TextField(null=False, blank=False, default=str(time.time()))
    validation_stage = models.CharField(max_length=50, choices=VALIDATION_STAGES)

    def __str__(self):
        """
        Returns a string representation of the article.

        Returns:
            str: The title of the article.
        """
        return self.title

    @property
    def article_language(self):
        """
        Property that detects the language of the article content.

        Returns:
            str: The detected language of the article content.
        """
        return detect_language(self.article_content)
