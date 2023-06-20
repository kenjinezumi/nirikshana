from django.db import models
import time
from apps.articles.utils import detect_language, validate_url


class Articles(models.Model):
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
        return self.title

    @property
    def article_language(self):
        return detect_language(self.article_content)





